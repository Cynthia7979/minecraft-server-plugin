import json
from mcpython.minecraft import Minecraft, CmdPlayer
from time import sleep

JSON_DATABSE_PATH = './book_of_locations.json'


def main():
    mc = Minecraft.create()
    try:
        conn = mc.conn
        print('Running!')
        mc.postToChat('')
        mc.postToChat('§9§k12§r§9 locations.py is up and running. Type §f?location §9to query the Book of Locations! §k22§r')
        mc.postToChat('')

        cmd_players = update_player_ids(mc, {})

        while True:  # Main loop
            database = json.load(open(JSON_DATABSE_PATH))

            # Update player entity IDs to fetch corresponding chatEvents
            cmd_players = update_player_ids(mc, cmd_players)

            # Handle chat messages
            for plr_id, cmd_plr in cmd_players.items():
                chat_events = cmd_plr.pollChatPosts()
                if chat_events: print(chat_events)
                for chat_event in chat_events:
                    msg = chat_event.message
                    args = msg.split()
                    if args[0] == '?location':
                        send_book_of_locations(mc, database)
                    elif args[0] == '?save':
                        save_player_pos(mc, cmd_plr, database)
                    elif args[0] == '?saveAs':
                        if len(args) > 1:
                            save_player_pos_as(mc, cmd_plr, ' '.join(args[1:]), database)
                        else:
                            mc.postToChat('§9You did not specify a pos type. The current pos types are:')
                            show_pos_types(mc, database)
                    elif args[0] == '?saveas':
                        mc.postToChat('§7Do you mean §f?saveAs §7?')
                    elif args[0] == '?query':
                        try:
                            pos_type = args[1]
                            assert pos_type in database.keys(), IndexError
                            send_typed_locations(mc, pos_type, database)
                        except IndexError:
                            mc.postToChat('§9Please provide a valid pos type. Current pos types are:§9')
                            show_pos_types(mc, database)
                    elif args[0] == '?help':
                        mc.postToChat('§9Available commands:')
                        mc.postToChat('§f?location - §7Show all saved locations')
                        mc.postToChat('§f?save - §7Save current player location as type default')
                        mc.postToChat('§f?saveAs <type> - §7Save current player location as the specified type')
                        mc.postToChat('§f?query <type> - §7Show all locations in the specified type')
                        mc.postToChat('§f?help - §7Show this manual§r')
                    elif msg.startswith('?'):
                        mc.postToChat(f'§7<locations.py> Command "{args[0]}" not found.')
            if len(cmd_players) == 0:
                sleep(10)  # Don't know why but maybe this could enhance performance?
            else:
                sleep(2)
    except Exception as e:
        mc.postToChat('§4<locations.py> An error occurred. The program is stopped.')
        assert 1 == 0, e


def update_player_ids(world, cmd_players: dict):
    conn = world.conn
    try:
        player_ids = world.getPlayerEntityIds()
    except ValueError:  # No players
        return {}
    for plrID in player_ids:
        if plrID not in cmd_players.keys():
            cmd_players[plrID] = CmdPlayer(conn, plrID)
    return cmd_players


def send_book_of_locations(world, json_):
    world.postToChat('§r')
    world.postToChat("§9>> Book Of Locations <<§r")
    for pos_type, pos_data in json_.items():
        world.postToChat(f"  §f{pos_type.capitalize()}")
        for line in pos_data:
            world.postToChat(f"    §7{line}")
    world.postToChat('§r')


def save_player_pos(world, cmd_player, json_):
    world.postToChat('§7Saving as "default" position. To specify position, call §f?saveAs <type>')
    save_player_pos_as(world, cmd_player, 'default', json_)


def save_player_pos_as(world, cmd_player, pos_type, json_):
    print(cmd_player.getEntities())
    player_pos_x, player_pos_y, player_pos_z = cmd_player.getPos()
    if pos_type in json_.keys():
        json_[pos_type].append(f'{int(player_pos_x)} {int(player_pos_z)}')
        json.dump(json_, open(JSON_DATABSE_PATH, 'w'), indent='    ')
    world.postToChat(f'§9Successfully saved ({int(player_pos_x)} {int(player_pos_z)}) as {pos_type}.')
    world.postToChat('§r')


def show_pos_types(world, json_):
    for pos_type in json_.keys():
        world.postToChat(f'§7  {pos_type}')
    world.postToChat('§r')


def send_typed_locations(world, pos_type, json_):
    world.postToChat(f'§f{pos_type}')
    for line in json_[pos_type]:
        world.postToChat(f'  §7{line}')
    world.postToChat('§r')


if __name__ == '__main__':
    main()
