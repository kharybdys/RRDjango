class Roborally {
    base_element_color = 'grey'; // note that grey is darker than darkgrey

    constructor(board_data, canvas_id) {
        this.board_data = board_data;
        this.element_size = this.board_data.factor * 12;
        this.factor = this.board_data.factor;
        this.board_canvas = new fabric.StaticCanvas(canvas_id);
        this._load_canvas()
    }
    
    _load_canvas() {
        this.board_canvas.setHeight(this.board_data.height * this.element_size);
        this.board_canvas.setWidth(this.board_data.width * this.element_size);
    }
    
    _draw_basic(data) {
        const element = new fabric.Rect({
          left: data.x * this.element_size,
          top: data.y * this.element_size,
          fill: this.base_element_color,
          width: this.element_size,
          height:  this.element_size,
          my_type : 'BASIC'
        });
        this.board_canvas.add(element);
    }

    _draw_with_symbol(data, symbol) {
        const outer = new fabric.Rect({
          fill: this.base_element_color,
          originX: 'center',
          originY: 'center',
          width: this.element_size,
          height:  this.element_size
        });

        // noinspection JSSuspiciousNameCombination
        const element = new fabric.Rect({
          fill: 'darkslategrey',
          width: this.element_size - 4 * this.factor,
          height:  this.element_size - 4 * this.factor,
          originX: 'center',
          originY: 'center'
        });

        const text = new fabric.Text(symbol, {
            stroke: 'white',
            fill: 'white',
            textAlign: 'center',
            fontSize: 4 * this.factor,
            originX: 'center',
            originY: 'center',
            my_type: 'SYMBOL'
        });

        const group = new fabric.Group([outer, element, text], {
          left: data.x * this.element_size,
          top: data.y * this.element_size,
          my_type: 'DRAW_SYMBOL'
        });

        this.board_canvas.add(group);
    }
    
    _draw_starting(data) {
        console.log('Drawing starting with data: ' + JSON.stringify(data))
        this._draw_with_symbol(data, String(data.symbol))
    }
    
    _draw_repair(data) {
        console.log('Drawing repair with data: ' + JSON.stringify(data))
        this._draw_with_symbol(data, 'R')
    }
    
    _draw_option(data) {
        console.log('Drawing option with data: ' + JSON.stringify(data))
        this._draw_with_symbol(data, 'O')
    }
    
    _draw_hole(data) {
        console.log('Drawing hole with data: ' + JSON.stringify(data))
        const element = new fabric.Rect({
          left: data.x * this.element_size,
          top: data.y * this.element_size,
          fill: 'black',
          width: this.element_size,
          height:  this.element_size,
          my_type: 'HOLE'
        });
        this.board_canvas.add(element);
    }

    _svg_command_to_str(command, x, y, dx, dy) {
        let result = command;
        if( typeof dx !== 'undefined' ) {
            result = result.concat(' ', dx.toString());
        }
        if( typeof dy !== 'undefined' ) {
            result = result.concat(' ', dy.toString());
        }
        if( typeof x !== 'undefined' ) {
            result = result.concat(' ', x.toString());
        }
        if( typeof y !== 'undefined' ) {
            result = result.concat(' ', y.toString());
        }
        return result;
    }

    _flip_command(command, flip) {
        if(flip) {
            let new_command = {};
            let new_command_type = command.command_type;
            if(command.command_type === 'H') {
                new_command_type = 'V';
            }
            if(command.command_type === 'V') {
                new_command_type = 'H';
            }
            new_command.command_type = new_command_type;
            if( typeof command.x !== 'undefined' ) {
                // noinspection JSSuspiciousNameCombination
                new_command.y = command.x;
            }
            if( typeof command.y !== 'undefined' ) {
                // noinspection JSSuspiciousNameCombination
                new_command.x = command.y;
            }
            if( typeof command.dx !== 'undefined' ) {
                // noinspection JSSuspiciousNameCombination
                new_command.dy = command.dx;
            }
            if( typeof command.dy !== 'undefined' ) {
                // noinspection JSSuspiciousNameCombination
                new_command.dx = command.dy;
            }
            return new_command;
        } else {
            return command;
        }
    }

    _transform_svg_path(path, transformX, transformY, flip=false) {
        let result = [];
        path.map((command) => { return this._flip_command(command, flip);})
            .forEach((command) => {
            let new_x = undefined;
            if( typeof command.x !== 'undefined' ) {
                new_x = transformX(command.x);
            }
            let new_y = undefined;
            if( typeof command.y !== 'undefined' ) {
                new_y = transformY(command.y);
            }
            let new_dx = undefined;
            if( typeof command.dx !== 'undefined' ) {
                new_dx = transformX(command.dx);
            }
            let new_dy = undefined;
            if( typeof command.dy !== 'undefined' ) {
                new_dy = transformY(command.dy);
            }
            result.push(this._svg_command_to_str(command.command_type, new_x, new_y, new_dx, new_dy));
        })
        return result.join(' ');
    }

    _to_svg_list(stringPath) {
        return stringPath.split(/ (?=[A-Z])/).map((command) => {
            const components = command.split(' ')[Symbol.iterator]();
            const command_type = components.next().value;
            const result = {'command_type': command_type};
            switch (command_type) {
                case('Z'):
                    break;
                case('M'):
                    result.x = components.next().value;
                    result.y = components.next().value;
                    break;
                case('V'):
                    result.y = components.next().value;
                    break;
                case('H'):
                    result.x = components.next().value;
                    break;
                case('L'):
                    result.x = components.next().value;
                    result.y = components.next().value;
                    break;
                case('Q'):
                    result.dx = components.next().value;
                    result.dy = components.next().value;
                    result.x = components.next().value;
                    result.y = components.next().value;
                    break;
                default:
                    throw new Error('I do not support the other SVG commands')
            }
            return result;
        });
    }

    _draw_conveyor(data, color, bentPath, straightPath) {
        console.log('Conveyor with data: ' + JSON.stringify(data));
        const rect = new fabric.Rect({
          fill: 'black',
          width: this.element_size,
          height: this.element_size
        });
        const conveyor_elements = [rect];
        const end_direction = data.end_direction;

        if( ! data.starting_directions.includes('SOUTH') && 'SOUTH' !== end_direction) {
            // noinspection JSSuspiciousNameCombination
            const side = new fabric.Rect({
              fill: color,
              left: 0,
              top: this.element_size - 2 * this.factor,
              strokeWidth: 0,
              width: this.element_size,
              height: 2 * this.factor
            });
            conveyor_elements.push(side);
        }
        if( ! data.starting_directions.includes('WEST') && 'WEST' !== end_direction) {
            const side = new fabric.Rect({
              fill: color,
              left: 0,
              top: 0,
              strokeWidth: 0,
              width: 2 * this.factor,
              height: this.element_size
            });
            conveyor_elements.push(side);
        }
        if( ! data.starting_directions.includes('NORTH') && 'NORTH' !== end_direction) {
            // noinspection JSSuspiciousNameCombination
            const side = new fabric.Rect({
              fill: color,
              left: 0,
              top: 0,
              strokeWidth: 0,
              width: this.element_size,
              height: 2 * this.factor
            });
            conveyor_elements.push(side);
        }
        if( ! data.starting_directions.includes('EAST') && 'EAST' !== end_direction) {
            const side = new fabric.Rect({
              fill: color,
              left: this.element_size - 2 * this.factor,
              top: 0,
              strokeWidth: 0,
              width: 2 * this.factor,
              height: this.element_size
            });
            conveyor_elements.push(side);
        }

        data.starting_directions.forEach((starting_direction) => {
            let arrowPath = undefined;
            let transformX = function(x) { return x; };
            let transformY = function(y) { return y; };
            if( end_direction === 'SOUTH') {
                if( starting_direction === 'WEST' ) {
                    transformX = function(x) { return 12 - x; };
                    arrowPath = this._transform_svg_path(bentPath, transformX, transformY, true);
                } else if( starting_direction === 'NORTH' ) {
                    transformX = function(x) { return 12 - x; };
                    arrowPath = this._transform_svg_path(straightPath, transformX, transformY, true);
                } else if( starting_direction === 'EAST' ) {
                    arrowPath = this._transform_svg_path(bentPath, transformX, transformY, true);
                } else {
                    throw Error( "Cannot start and exit in the same direction!" )
                }
            } else if( end_direction === 'WEST') {
                if( starting_direction === 'NORTH' ) {
                    transformX = function(x) { return 12 - x; };
                    transformY = function(y) { return 12 - y; };
                    arrowPath = this._transform_svg_path(bentPath, transformX, transformY);
                } else if( starting_direction === 'EAST' ) {
                    transformX = function(x) { return 12 - x; };
                    arrowPath = this._transform_svg_path(straightPath, transformX, transformY);
                } else if( starting_direction === 'SOUTH' ) {
                    transformX = function(x) { return 12 - x; };
                    arrowPath = this._transform_svg_path(bentPath, transformX, transformY);
                } else {
                    throw Error( "Cannot start and exit in the same direction!" )
                }
            } else if( end_direction === 'NORTH') {
                if (starting_direction === 'EAST') {
                    transformY = function(y) { return 12 - y; };
                    arrowPath = this._transform_svg_path(bentPath, transformX, transformY, true);
                } else if (starting_direction === 'SOUTH') {
                    transformY = function(y) { return 12 - y; };
                    arrowPath = this._transform_svg_path(straightPath, transformX, transformY, true);
                } else if (starting_direction === 'WEST') {
                    transformX = function(x) { return 12 - x; };
                    transformY = function(y) { return 12 - y; };
                    arrowPath = this._transform_svg_path(bentPath, transformX, transformY, true);
                } else {
                    throw Error("Cannot start and exit in the same direction!")
                }
            } else if( end_direction === 'EAST') {
                if (starting_direction === 'SOUTH') {
                    arrowPath = this._transform_svg_path(bentPath, transformX, transformY);
                } else if (starting_direction === 'WEST') {
                    arrowPath = this._transform_svg_path(straightPath, transformX, transformY);
                } else if (starting_direction === 'NORTH') {
                    transformY = function(y) { return 12 - y; };
                    arrowPath = this._transform_svg_path(bentPath, transformX, transformY);
                } else {
                    throw Error("Cannot start and exit in the same direction!")
                }
            }
            console.log('starting_direction: ' + starting_direction + ', arrowPath: ' + arrowPath);
            const element = new fabric.Path(arrowPath, {
              fill: color,
              scaleX: this.factor,
              scaleY: this.factor,
              strokeWidth: 0
            });

            console.log('width: ' + element.getScaledWidth() + ', height:' + element.getScaledHeight() );

            conveyor_elements.push(element);
        });

        const group = new fabric.Group(conveyor_elements, {
          left: data.x * this.element_size,
          top: data.y * this.element_size,
          my_type: 'CONVEYOR'
        });

        this.board_canvas.add(group);
    }

    _draw_single_conveyor(data) {
        // starts west, ends east. Straight
        const straightArrowPath = this._to_svg_list("M 1 5 H 10 V 4 L 11 6 L 10 8 V 7 H 1 Z M 0 0 H 2 V 2 H 0 Z M 0 12 H 2 V 10 H 0 Z M 12 12 V 10 H 10 V 12 Z M 12 0 V 2 H 10 V 0 Z");
        // starts south, ends east. Curved.
        const bentArrowPath = this._to_svg_list("M 5 11 V 9 Q 5 5 9 5 H 10 V 4 L 11 6 L 10 8 V 7 H 9 Q 7 7 7 9 V 11 Z M 0 12 V 10 H 2 V 12 Z M 12 12 V 10 H 10 V 12 Z M 0 0 V 2 H 2 V 0 Z M 12 0 V 2 H 10 V 0 Z");
        this._draw_conveyor(data, 'orange', bentArrowPath, straightArrowPath);
    }
    
    _draw_dual_conveyor(data) {
        // starts west, ends east. Straight
        const straightArrowPath = this._to_svg_list("M 1 5 H 9 V 4 L 10 6 V 4 L 11 6 L 10 8 V 6 L 9 8 V 7 H 1 Z M 0 0 H 2 V 2 H 0 Z M 10 12 H 12 V 10 H 10 Z M 0 12 V 10 H 2 V 12 Z M 12 0 V 2 H 10 V 0 Z");
        // starts south, ends east. Curved.
        const bentArrowPath = this._to_svg_list("M 5 11 V 9 Q 5 5 9 5 V 4 L 10 6 H 10 V 4 L 11 6 L 10 8 V 6 L 9 8 H 9 V 7 Q 7 7 7 9 V 11 Z M 0 12 V 10 H 2 V 12 Z M 12 12 V 10 H 10 V 12 Z M 0 0 V 2 H 2 V 0 Z M 12 0 V 2 H 10 V 0 Z");
        this._draw_conveyor(data, 'SteelBlue', bentArrowPath, straightArrowPath);
    }
    
    _draw_pusher(data) {
        console.log('Drawing pusher with data: ' + JSON.stringify(data));
        const pusherThreePath = this._to_svg_list("M 0 0 H 12 V 1 H 3 V 2 H 5 V 1 H 7 V 2 H 9 V 1 H 11 V 2 H 12 V 3 H 0 V 2 H 1 V 1 H 0 Z");
        const pusherTwoPath = this._to_svg_list("M 0 0 H 12 V 1 H 4 V 2 H 8 V 1 H 10 V 2 H 12 V 3 H 0 V 2 H 2 V 1 H 0 Z");
        let pusherPath = undefined;
        if( data.element_type === 'PUSHER_135' ) {
            pusherPath = pusherThreePath;
        } else {
            pusherPath = pusherTwoPath;
        }
        let path = undefined;
        let left = 0;
        let top = 0;
        let transformX = function(x) { return x; };
        let transformY = function(y) { return y; };
        if( data.direction === 'EAST') {
            path = this._transform_svg_path(pusherPath, transformX, transformY, true);
        } else if( data.direction === 'SOUTH') {
            path = this._transform_svg_path(pusherPath, transformX, transformY, false);
        } else if( data.direction === 'WEST') {
            transformX = function(x) { return 12 - x; };
            path = this._transform_svg_path(pusherPath, transformX, transformY, true);
            left = 9 * this.factor;
        } else if( data.direction === 'NORTH') {
            transformY = function(y) { return 12 - y; };
            path = this._transform_svg_path(pusherPath, transformX, transformY, false);
            top = 9 * this.factor;
        } else {
            throw Error( "Unknown direction: " + data.direction )
        }

        const background = new fabric.Rect({
          fill: this.base_element_color,
          width: this.element_size,
          height:  this.element_size
        });

        const element = new fabric.Path(path, {
          left: left,
          top: top,
          fill: 'darkslategrey',
          scaleX: this.factor,
          scaleY: this.factor,
          strokeWidth: 0
        });

        const group = new fabric.Group([ background, element ], {
          left: data.x * this.element_size,
          top: data.y * this.element_size,
          my_type: 'PUSHER'
        });

        this.board_canvas.add(group);
    }

    _draw_rotator(data, path, color) {
        const background = new fabric.Rect({
          fill: this.base_element_color,
          width: this.element_size,
          height:  this.element_size
        });

        const outer_circle = new fabric.Circle({
          radius: 5 * this.factor,
          fill: 'lightgrey',
          left: this.factor,
          top: this.factor
        });

        const rotator = new fabric.Path(path, {
          top: 1 * this.factor,
          left: 2 * this.factor,
          fill: color,
          scaleX: this.factor,
          scaleY: this.factor,
          strokeWidth: 0
        });

        const group = new fabric.Group([ background, outer_circle, rotator ], {
          left: data.x * this.element_size,
          top: data.y * this.element_size,
          my_type: 'ROTATOR'
        });
        this.board_canvas.add(group);
    }
    
    _draw_rotator_clockwise(data) {
        console.log('Drawing clockwise rotator with data: ' + JSON.stringify(data))
        const path = "M 6 2 Q 2 2 2 6 H 4 Q 4 4 6 4 V 5 L 7 3 L 6 1 Z M 6 10 Q 10 10 10 6 H 8 Q 8 8 6 8 V 7 L 5 9 L 6 11 Z";
        this._draw_rotator(data, path, 'darkgreen');
    }
    
    _draw_rotator_counter_clockwise(data) {
        console.log('Drawing counter clockwise rotator with data: ' + JSON.stringify(data))
        const path = "M 6 2 Q 10 2 10 6 H 8 Q 8 4 6 4 V 5 L 5 3 L 6 1 Z M 6 10 Q 2 10 2 6 H 4 Q 4 8 6 8 V 7 L 7 9 L 6 11 Z";
        this._draw_rotator(data, path, 'darkred');
    }
    
    _draw_bot(data) {
        console.log('Drawing bot with data: ' + JSON.stringify(data))

    }
    
    _draw_flag(data) {
        console.log('Drawing flag with data: ' + JSON.stringify(data))
        let flag_color = 'lime'
        let text_color = 'lime'
        let flag_elements = []
        flag_elements.push(new fabric.Line([data.x * this.element_size + 3 * this.factor,
                data.y * this.element_size + 3 * this.factor,
                data.x * this.element_size + 3 * this.factor,
                data.y * this.element_size + 12 * this.factor],
            { fill: flag_color,
              stroke: flag_color,
              strokeWidth: this.factor
            }))
        flag_elements.push(new fabric.Line([data.x * this.element_size + 3 * this.factor,
                data.y * this.element_size + 3 * this.factor,
                data.x * this.element_size + 10 * this.factor,
                data.y * this.element_size + 3 * this.factor],
            { fill: flag_color,
              stroke: flag_color,
              strokeWidth: this.factor
            }))
        flag_elements.push(new fabric.Line([data.x * this.element_size + 3 * this.factor,
                data.y * this.element_size + 8 * this.factor,
                data.x * this.element_size + 11 * this.factor,
                data.y * this.element_size + 8 * this.factor],
            { fill: flag_color,
              stroke: flag_color,
              strokeWidth: this.factor
            }))
        flag_elements.push(new fabric.Line([data.x * this.element_size + 10 * this.factor,
                data.y * this.element_size + 3 * this.factor,
                data.x * this.element_size + 10 * this.factor,
                data.y * this.element_size + 9 * this.factor],
            { fill: flag_color,
              stroke: flag_color,
              strokeWidth: this.factor
            }))

        flag_elements.push(new fabric.Text(data.symbol, {
            stroke: text_color,
            fill: text_color,
            textAlign: 'center',
            fontSize: 4 * this.factor,
            left: data.x * this.element_size + this.factor,
            top: data.y * this.element_size + this.factor,
            my_type: 'SYMBOL'
        }));

        const group = new fabric.Group(flag_elements, {
          my_type: 'FLAG'
        });

        this.board_canvas.add(group);
    }
    
    _create_laser_elements(data) {
        console.log('Drawing laser with data: ' + JSON.stringify(data))
        let laserPath = "M 12 0 Q 6 2 0 0 Z";
        let transformX = function(x) { return x; };
        let transformY = function(y) { return y; };
        let x_correction = 0;
        let y_correction = 0;
        if( data.direction === 'EAST') {
            laserPath = this._transform_svg_path(this._to_svg_list(laserPath), transformX, transformY, true);
            x_correction = this.factor;
        } else if( data.direction === 'NORTH') {
            transformY = function (y) { return 12 - y; };
            laserPath = this._transform_svg_path(this._to_svg_list(laserPath), transformX, transformY);
            y_correction = 10 * this.factor;
        } else if( data.direction === 'WEST') {
            transformX = function (x) { return 12 - x; };
            laserPath = this._transform_svg_path(this._to_svg_list(laserPath), transformX, transformY, true);
            x_correction = 10 * this.factor;
        } else if( data.direction === 'SOUTH') {
            y_correction = this.factor;
        } else {
            throw Error( "Unknown direction: " + data.direction )
        }
        const element = new fabric.Path(laserPath, {
          fill: 'red',
          scaleX: this.factor,
          scaleY: this.factor,
          strokeWidth: 0,
          left: data.x * this.element_size + x_correction,
          top: data.y * this.element_size + y_correction,
          my_type: 'LASER_MOUNT'
        });
        const laser_path = [element];
        data.laser_path.forEach((field) => {
            for (let i = 0; i < data.hits; i++) {
                let coordinates;
                let correction = this.factor * ( 6 - (data.hits - 1) + 2 * i);
                if( data.direction === 'SOUTH' || data.direction === 'NORTH') {
                    coordinates = [field.x * this.element_size + correction, (field.y + 0) * this.element_size,
                                   field.x * this.element_size + correction, (field.y + 1) * this.element_size];
                } else {
                    coordinates = [(field.x + 0) * this.element_size, field.y * this.element_size + correction,
                                   (field.x + 1) * this.element_size, field.y * this.element_size + correction];
                }
                laser_path.push( new fabric.Line(coordinates,
                    { fill: 'red',
                      stroke: 'red',
                      strokeWidth: 2
                    }))
            }
        })
        return laser_path;
    }

    _create_wall_element(data) {
        console.log('Drawing wall with data: ' + JSON.stringify(data))
        let width = undefined;
        let height = undefined;
        let top = undefined;
        let left = undefined;
        if(data.direction === 'SOUTH') {
            width = this.element_size;
            height = this.factor;
            left = data.x * this.element_size;
            top = (data.y + 1) * this.element_size - this.factor;
        } else if(data.direction === 'WEST') {
            width = this.factor;
            height = this.element_size;
            left = data.x * this.element_size;
            top = data.y * this.element_size;
        } else if(data.direction === 'NORTH') {
            width = this.element_size;
            height = this.factor;
            left = data.x * this.element_size;
            top = data.y * this.element_size;
        } else if(data.direction === 'EAST') {
            width = this.factor;
            height = this.element_size;
            left = (data.x + 1) * this.element_size - this.factor;
            top = data.y * this.element_size;
        }

        return new fabric.Rect({
          fill: 'yellow',
          width: width,
          height: height,
          left: left,
          top: top
        });
    }
    
    draw_canvas() {

        this.board_data.elements.forEach((element) => {
            switch(element.element_type) {
                case 'BasicElement':
                    this._draw_basic(element);
                    break;
                case 'StartingElement':
                    this._draw_starting(element);
                    break;
                case 'RepairElement':
                    this._draw_repair(element);
                    break;
                case 'OptionElement':
                    this._draw_option(element);
                    break;
                case 'HoleElement':
                    this._draw_hole(element);
                    break;
                case 'SingleSpeedConveyor':
                    this._draw_single_conveyor(element);
                    break;
                case 'DualSpeedConveyor':
                    this._draw_dual_conveyor(element);
                    break;
                case 'Pusher135':
                case 'Pusher24':
                    this._draw_pusher(element);
                    break;
                case 'ClockwiseRotator':
                    this._draw_rotator_clockwise(element);
                    break;
                case 'CounterClockwiseRotator':
                    this._draw_rotator_counter_clockwise(element);
                    break;
                default:
                    console.error('Unsupported element_type ' + element.element_type);
            }
        });
        const laser_elements = [];
        this.board_data.lasers.forEach((laser) => {
            laser_elements.push(...this._create_laser_elements(laser));
        });
        const lasers = new fabric.Group(laser_elements, {my_type : 'LASER'});
        this.board_canvas.add(lasers);
        // walls after lasers so the laser correctly starts and ends in the wall
        const wall_elements = [];
        this.board_data.walls.forEach((wall) => {
           wall_elements.push(this._create_wall_element(wall));
        });
        const walls = new fabric.Group(wall_elements, {my_type : 'WALL'});
        this.board_canvas.add(walls);
        this.board_data.movables.forEach((movable) => {
            switch(movable.movable_type) {
                case 'Flag':
                    this._draw_flag(movable)
                    break;
                case 'Bot':
                    this._draw_bot(movable)
                    break;
                default:
                    console.error('Unsupported movable_type ' + movable.movable_type);
            }
        });
    }
}

