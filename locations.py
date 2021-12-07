import mcpython
from mcpython.minecraft import Minecraft, CmdPlayer
from time import sleep


def main():
    mc = Minecraft.create()
    conn = mc.conn
    print('Running!')
    mc.postToChat('')
    mc.postToChat('§9§k1322§r§9 locations.py is up and running. Type ?location to query the Book of Locations!§k1322§r')
    mc.postToChat('')

    cmd_players = update_player_ids(mc, {})

    while True:
        # Update player entity IDs to fetch corresponding chatEvents
        cmd_players = update_player_ids(mc, cmd_players)
        chat_per_player = [plr.pollChatPosts() for plr in cmd_players.values()]  # Fetch chat for each player
        chat_events = [e for chat_list in chat_per_player for e in chat_list]  # Flatten out list
        if chat_events: print(chat_events)
        for chat_event in chat_events:
            if chat_event.message == '?location':
                mc.postToChat('')
                mc.postToChat("§9>> Book Of Locations <<§9")
                for line in open('./book_of_locations.txt', encoding='utf-8').readlines():
                    mc.postToChat("    "+line)
                mc.postToChat('')
        sleep(2)


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


if __name__ == '__main__':
    main()
