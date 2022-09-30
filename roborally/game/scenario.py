"""
Java implementation
    public static enum ImplementedScenario
    {
         MovingTargets,
         Test,
         AgainstTheGrain,
         Tricksy,
         IslandKing,
         OddestSea,
         RobotStew,
         LostBearings,
         WhirlwindTour,
         VaultAssault,
         Pilgrimage,
         DeathTrap,
         AroundTheWorld,
         BloodbathChess,
         Twister,
         ChopShopChallenge,
         IslandHop,
         DizzyDash,
         Checkmate,
         RiskyExchange
    }

    @Inject
    private Logger log;

    private List<RoboRallyBoard> boards;
    private int xSize;
    private int ySize;
    private List<Flag> flags;
    private Map<Integer, Bot> bots;
    private static final RoboRallyBoardElement outsideElement = new BasicElement(-1, -1, null, null, (List<RoboRallyDirection>) null, 0, AbstractBoardElement.BoardElementType.HOLE);

    public RoboRallyScenario(int xSize, int ySize, List<RoboRallyBoard> boards) {
        this.boards = boards;
        this.xSize = xSize;
        this.ySize = ySize;
        this.flags = new ArrayList<Flag>();
        this.bots = new HashMap<Integer, Bot>();
    }

    public Dimension getDimension(int factor)
    {
        return new Dimension(xSize*factor*AbstractBoardElement.baseSize, ySize*factor*AbstractBoardElement.baseSize);
    }

    public void setBotCoords(int botNumber, Coordinates coords)
    {
        Bot bot = bots.get(botNumber);
        if (bot != null) {
            bot.setCoords(coords);
        }
    }

    public Coordinates getBotCoords(int botNumber)
    {
        Bot bot = bots.get(botNumber);
        if (bot != null) {
            return bot.getCoords();
        } else {
            return null;
        }
    }

    public void setBotXCoord(int botNumber, int newX) {
        Bot bot = bots.get(botNumber);
        if (bot != null) {
            bot.setxCoord(newX);
        }
    }

    public int getBotXCoord(int botNumber) {
        Bot bot = bots.get(botNumber);
        if (bot != null) {
            return bot.getxCoord();
        } else {
            return -1;
        }
    }

    public void setBotYCoord(int botNumber, int newY) {
        Bot bot = bots.get(botNumber);
        if (bot != null) {
            bot.setyCoord(newY);
        }
    }

    public int getBotYCoord(int botNumber) {
        Bot bot = bots.get(botNumber);
        if (bot != null) {
            return bot.getyCoord();
        } else {
            return -1;
        }
    }

    public void setFlags(List<Flag> flags)
    {
        this.flags = flags;
    }

    public void setBots(List<Bot> bots)
    {
        for (Bot b : bots)
        {
            this.bots.put(b.getOrderNumber(), b);
        }
    }

    public boolean outOfYBounds(int y)
    {
        return y<0 || y>=ySize;
    }

    public boolean outOfXBounds(int x)
    {
        return x<0 || x>=xSize;
    }

    public boolean outOfBounds(Coordinates coords)
    {
        return outOfXBounds(coords.getxCoord()) || outOfYBounds(coords.getyCoord());
    }

    public boolean existsBot(int botNumber)
    {
        return bots != null && bots.containsKey(botNumber);
    }

    public Bot getBotOn(Coordinates coords)
    {
        for (Bot b : bots.values())
        {
            if (b.getCoords().equals(coords))
            {
                return b;
            }
        }
        return null;
    }

    public RoboRallyBoardElement getBoardElement(Coordinates coords)
    {
        return getBoardElement(coords.getxCoord(), coords.getyCoord());
    }

    public RoboRallyBoardElement getBoardElement(Integer xCoord, Integer yCoord) {
        for (RoboRallyBoard board : boards)
        {
            if ((xCoord >= board.getxOffset()) && (xCoord < (board.getxOffset() + board.getxSize())))
            {
                if ((yCoord >= board.getyOffset()) && (yCoord < (board.getyOffset() + board.getySize())))
                {
                    return board.getElement(xCoord - board.getxOffset(), yCoord - board.getyOffset());
                }
            }
        }
        // not found on any of the existing boards so it must be outside.
        return outsideElement;
    }

    public static BufferedImage getPreviewImage(ImplementedScenario scenarioName, boolean standardFlags, List<Flag> flags, List<Bot> bots, int factor) {
        RoboRallyScenario scenario = RoboRallyFactory.getInstance().getScenario(scenarioName);
        if (standardFlags)
        {
            scenario.setFlags(RoboRallyFactory.getInstance().getStandardFlags(scenarioName));
        }
        else
        {
            scenario.setFlags(flags);
        }
        if (bots!=null)
        {
            scenario.setBots(bots);
        }
        else
        {
            List<Bot> standardBots = new ArrayList<Bot>();
            standardBots.add(scenario.getInitialBot(1));
            standardBots.add(scenario.getInitialBot(2));
            standardBots.add(scenario.getInitialBot(3));
            scenario.setBots(standardBots);
        }
        return scenario.getImage(factor);
    }

    public Bot getInitialBot(int number)
    {
        int x = 0;
        int y = 0;
        boolean found=false;
        for (RoboRallyBoard board : boards)
        {
            int i=0;
            while (i<board.getxSize() && !found)
            {
                int j=0;
                while (j<board.getySize() && !found)
                {
                    RoboRallyBoardElement element = board.getElement(i, j);
                    if (element instanceof BasicElement)
                    {
                        if(AbstractBoardElement.BoardElementType.STARTING.equals(element.getBoardElementType()) && number==(((BasicElement) element).getNumber()))
                        {
                            found=true;
                            x = board.getxOffset()+i;
                            y = board.getyOffset()+j;
                        }
                    }
                    if (!found)
                    {
                        j++;
                    }
                }
                if (!found)
                {
                    i++;
                }
            }
        }
        return Bot.getBot(x, y, number, "Bot " + number);
    }

    public BufferedImage getImage(int factor) {
        int w = (xSize+2)*factor*AbstractBoardElement.baseSize;
        int h = (ySize+2)*factor*AbstractBoardElement.baseSize;
        BufferedImage bi = new BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB);
        Graphics g = bi.getGraphics();
        g.setColor(new Color(31, 31, 31));
        g.fillRect(0, 0, w, h);
        g.translate(factor*AbstractBoardElement.baseSize, factor*AbstractBoardElement.baseSize);
        this.paint(g, factor);
        g.dispose();
        return bi;
    }

    public void paint(Graphics g, int factor) {
        int w = xSize*factor*AbstractBoardElement.baseSize;
        int h = ySize*factor*AbstractBoardElement.baseSize;
        Graphics2D g2d = (Graphics2D) g;
        g2d.translate(Math.max((w - xSize * AbstractBoardElement.baseSize * factor) / 2, 0), Math.max((h - ySize * AbstractBoardElement.baseSize * factor) / 2, 0));
        for (RoboRallyBoard board : boards) {
            board.paint(g, ySize * AbstractBoardElement.baseSize * factor, factor);
        }
        // paint flags first then bots so the bots actually show
        for (Flag flag : flags) {
            flag.paint(g, ySize * AbstractBoardElement.baseSize * factor, factor);
        }
        // TODO, if a bot is on a flag, should the flag number be visible somewhere? But how then.
        for (Bot bot : bots.values()) {
            if (bot!=null)
            {
                bot.paint(g, ySize * AbstractBoardElement.baseSize * factor, factor);
            }
        }
    }


    public void processDamageFromWallLaserForBot(Bot beingShot)
    {
        RoboRallyBoardElement startingElement = beingShot.getBoardElement();
        List<RoboRallyDirection> laserFire = startingElement.getDirectionLaserFire();
        if (laserFire != null && !laserFire.isEmpty())
        {
            for (RoboRallyDirection directionLaserFire : laserFire)
            { // directionLaserFire is the direction the laser fire is coming from.
              // thus we check if there isn't another bot in that direction. Checking should stop at wall or mount (typically both exist at the same spot)
                Coordinates currentCoords = beingShot.getCoords();
                RoboRallyBoardElement currentElement = getBoardElement(currentCoords);
                Boolean hit = true;
                while (hit && !currentElement.existsLaserMount(directionLaserFire) && !currentElement.hasWall(directionLaserFire))
                {
                    // do we have a bot instead (unequal to beingShot)?
                    Bot blockingBot = getBotOn(currentCoords);
                    if (blockingBot != null && !blockingBot.equals(beingShot))
                    {
                        hit = false; // blockingBot takes the hit
                    }
                    // move one element in that direction
                    currentCoords = currentCoords.getNeighbouringCoordinates(directionLaserFire);
                    if (outOfBounds(currentCoords))
                    {
                        log.severe("Problem at board design, wall laser going off the board at coords " + currentCoords);
                        throw new RuntimeException("Board design problem, wall laser going off the board.");
                    }
                    currentElement = getBoardElement(currentCoords);
                }
                if (hit)
                {
                    beingShot.setDamage(beingShot.getDamage() + startingElement.getLaserDamage(directionLaserFire));
                    log.info("Bot " + beingShot + " just took " + startingElement.getLaserDamage(directionLaserFire) + " damage from " + directionLaserFire + " direction.");
                }
            }
        }
    }
"""