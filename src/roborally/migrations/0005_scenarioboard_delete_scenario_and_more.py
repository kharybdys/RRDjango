# Generated by Django 4.1 on 2022-12-17 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roborally', '0004_boardelement_scenario_scenarioflag'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScenarioBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('MOVING_TARGETS', 'Moving Targets'), ('AGAINST_THE_GRAIN', 'Against The Grain'), ('TRICKSY', 'Tricksy'), ('ISLAND_KING', 'Island King'), ('ODDEST_SEA', 'Oddest Sea'), ('ROBOT_STEW', 'Robot Stew'), ('LOST_BEARINGS', 'Lost Bearings'), ('WHIRLWIND_TOUR', 'Whirlwind Tour'), ('VAULT_ASSAULT', 'Vault Assault'), ('PILGRIMAGE', 'Pilgrimage'), ('DEATH_TRAP', 'Death Trap'), ('AROUND_THE_WORLD', 'Around The World'), ('BLOODBATH_CHESS', 'Bloodbath Chess'), ('TWISTER', 'Twister'), ('CHOP_SHOP_CHALLENGE', 'Chop Shop Challenge'), ('ISLAND_HOP', 'Island Hop'), ('DIZZY_DASH', 'Dizzy Dash'), ('CHECKMATE', 'Checkmate'), ('RISKY_EXCHANGE', 'Risky Exchange'), ('SET_TO_KILL', 'Set To Kill'), ('FACTORY_REJECTS', 'Factory Rejects'), ('OPTION_WORLD', 'Option World'), ('TIGHT_COLLAR', 'Tight Collar'), ('BALL_LIGHTNING', 'Ball Lightning'), ('DAY_OF_THE_SUPERBOT', 'Day Of The Superbot'), ('INTERFERENCE', 'Interference'), ('FLAG_FRY', 'Flag Fry'), ('FRENETIC_FACTORY', 'Frenetic Factory'), ('MARATHON_MADNESS', 'Marathon Madness'), ('TANDEM_CARNAGE', 'Tandem Carnage'), ('ALL_FOR_ONE', 'All For One'), ('CAPTURE_THE_FLAG', 'Capture The Flag'), ('TOGGLE_BOGGLE', 'Toggle Boggle'), ('WAR_ZONE', 'War Zone')], max_length=50)),
                ('turns', models.IntegerField(default=0)),
                ('offset_x', models.IntegerField(default=0)),
                ('offset_y', models.IntegerField(default=0)),
                ('board_name', models.CharField(choices=[('STARTING_BOARD_1', 'Starting Board 1'), ('STARTING_BOARD_2', 'Starting Board 2'), ('MAELSTROM', 'Maelstrom'), ('SPIN_ZONE', 'Spin Zone'), ('VAULT', 'Vault'), ('CROSS', 'Cross'), ('CHESS', 'Chess'), ('CHOP_SHOP', 'Chop Shop'), ('ISLAND', 'Island'), ('EXCHANGE', 'Exchange')], max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Scenario',
        ),
        migrations.AlterField(
            model_name='boardelement',
            name='element_type',
            field=models.CharField(choices=[('BASIC', 'Basic'), ('STARTING_1', 'Starting 1'), ('STARTING_2', 'Starting 2'), ('STARTING_3', 'Starting 3'), ('STARTING_4', 'Starting 4'), ('STARTING_5', 'Starting 5'), ('STARTING_6', 'Starting 6'), ('STARTING_7', 'Starting 7'), ('STARTING_8', 'Starting 8'), ('REPAIR', 'Repair'), ('OPTION', 'Option'), ('HOLE', 'Hole'), ('SINGLE_CONVEYOR', 'Single Conveyor'), ('DUAL_CONVEYOR', 'Dual Conveyor'), ('PUSHER_135', 'Pusher 135'), ('PUSHER_24', 'Pusher 24'), ('ROTATOR_CLOCKWISE', 'Rotator Clockwise'), ('ROTATOR_COUNTERCLOCKWISE', 'Rotator Counterclockwise'), ('WALL', 'Wall'), ('LASER', 'Laser')], max_length=50),
        ),
        migrations.AlterField(
            model_name='boardelement',
            name='name',
            field=models.CharField(choices=[('STARTING_BOARD_1', 'Starting Board 1'), ('STARTING_BOARD_2', 'Starting Board 2'), ('MAELSTROM', 'Maelstrom'), ('SPIN_ZONE', 'Spin Zone'), ('VAULT', 'Vault'), ('CROSS', 'Cross'), ('CHESS', 'Chess'), ('CHOP_SHOP', 'Chop Shop'), ('ISLAND', 'Island'), ('EXCHANGE', 'Exchange')], max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='scenario_name',
            field=models.CharField(choices=[('MOVING_TARGETS', 'Moving Targets'), ('AGAINST_THE_GRAIN', 'Against The Grain'), ('TRICKSY', 'Tricksy'), ('ISLAND_KING', 'Island King'), ('ODDEST_SEA', 'Oddest Sea'), ('ROBOT_STEW', 'Robot Stew'), ('LOST_BEARINGS', 'Lost Bearings'), ('WHIRLWIND_TOUR', 'Whirlwind Tour'), ('VAULT_ASSAULT', 'Vault Assault'), ('PILGRIMAGE', 'Pilgrimage'), ('DEATH_TRAP', 'Death Trap'), ('AROUND_THE_WORLD', 'Around The World'), ('BLOODBATH_CHESS', 'Bloodbath Chess'), ('TWISTER', 'Twister'), ('CHOP_SHOP_CHALLENGE', 'Chop Shop Challenge'), ('ISLAND_HOP', 'Island Hop'), ('DIZZY_DASH', 'Dizzy Dash'), ('CHECKMATE', 'Checkmate'), ('RISKY_EXCHANGE', 'Risky Exchange'), ('SET_TO_KILL', 'Set To Kill'), ('FACTORY_REJECTS', 'Factory Rejects'), ('OPTION_WORLD', 'Option World'), ('TIGHT_COLLAR', 'Tight Collar'), ('BALL_LIGHTNING', 'Ball Lightning'), ('DAY_OF_THE_SUPERBOT', 'Day Of The Superbot'), ('INTERFERENCE', 'Interference'), ('FLAG_FRY', 'Flag Fry'), ('FRENETIC_FACTORY', 'Frenetic Factory'), ('MARATHON_MADNESS', 'Marathon Madness'), ('TANDEM_CARNAGE', 'Tandem Carnage'), ('ALL_FOR_ONE', 'All For One'), ('CAPTURE_THE_FLAG', 'Capture The Flag'), ('TOGGLE_BOGGLE', 'Toggle Boggle'), ('WAR_ZONE', 'War Zone')], max_length=250),
        ),
        migrations.AlterField(
            model_name='scenarioflag',
            name='name',
            field=models.CharField(choices=[('MOVING_TARGETS', 'Moving Targets'), ('AGAINST_THE_GRAIN', 'Against The Grain'), ('TRICKSY', 'Tricksy'), ('ISLAND_KING', 'Island King'), ('ODDEST_SEA', 'Oddest Sea'), ('ROBOT_STEW', 'Robot Stew'), ('LOST_BEARINGS', 'Lost Bearings'), ('WHIRLWIND_TOUR', 'Whirlwind Tour'), ('VAULT_ASSAULT', 'Vault Assault'), ('PILGRIMAGE', 'Pilgrimage'), ('DEATH_TRAP', 'Death Trap'), ('AROUND_THE_WORLD', 'Around The World'), ('BLOODBATH_CHESS', 'Bloodbath Chess'), ('TWISTER', 'Twister'), ('CHOP_SHOP_CHALLENGE', 'Chop Shop Challenge'), ('ISLAND_HOP', 'Island Hop'), ('DIZZY_DASH', 'Dizzy Dash'), ('CHECKMATE', 'Checkmate'), ('RISKY_EXCHANGE', 'Risky Exchange'), ('SET_TO_KILL', 'Set To Kill'), ('FACTORY_REJECTS', 'Factory Rejects'), ('OPTION_WORLD', 'Option World'), ('TIGHT_COLLAR', 'Tight Collar'), ('BALL_LIGHTNING', 'Ball Lightning'), ('DAY_OF_THE_SUPERBOT', 'Day Of The Superbot'), ('INTERFERENCE', 'Interference'), ('FLAG_FRY', 'Flag Fry'), ('FRENETIC_FACTORY', 'Frenetic Factory'), ('MARATHON_MADNESS', 'Marathon Madness'), ('TANDEM_CARNAGE', 'Tandem Carnage'), ('ALL_FOR_ONE', 'All For One'), ('CAPTURE_THE_FLAG', 'Capture The Flag'), ('TOGGLE_BOGGLE', 'Toggle Boggle'), ('WAR_ZONE', 'War Zone')], max_length=50),
        ),
    ]
