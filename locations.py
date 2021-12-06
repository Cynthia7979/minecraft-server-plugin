import mcpython
from mcpython.minecraft import Minecraft, CmdPlayer
from time import sleep

mc = Minecraft.create()
conn = mc.conn
print('Running!')
mc.postToChat('')
mc.postToChat('§k12313322§r locations.py is up and running. Type ?location to query the Book of Locations!§k12313322')
mc.postToChat('')

while True:
    # get chat post events (messages) since the last time the function was run
    chatEvents = CmdPlayer(conn).pollChatPosts()
    if chatEvents: print(chatEvents)
    for chatEvent in chatEvents:
        if chatEvent.message == '?location':
            mc.postToChat('')
            mc.postToChat("§9>> Book Of Locations <<§r")
            for line in open('./book_of_locations.txt', encoding='utf-8').readlines():
                mc.postToChat("    "+line)
            mc.postToChat('')
    sleep(2)
