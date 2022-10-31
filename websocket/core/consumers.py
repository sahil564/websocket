import json
from multiprocessing import Event
from asgiref.sync import async_to_sync, sync_to_async

from time import sleep
import asyncio
from channels.consumer import SyncConsumer,AsyncConsumer

class MySyncConsumer(SyncConsumer):
    
    # this is handler is called when client initailly opns a
    #connetions and is about to finish the webSocket handshake
    def websocket_connect(self,evet):
         print("Websocket Connected...")
         print("channel layer...",self.channel_layer)# channel name 
         print("channel name...",self.channel_name)# group name 
         async_to_sync(self.channel_layer.group_add)(
             "programmers",
             self.channel_name
         )
         self.send({
             'type':"websocket.accept"
         })
         
    #this handler is called when data received from client     
    def websocket_receive(self,event):
        print("message Received..",event)
        print("Messaged is ",event['text'])
        for i in range(10):
            self.send({
                'type':'websocket.send',
                # 'text': str(i)
                'text':json.dumps({'count':i})
            })
            sleep(1)
    
    #this handler is called when either connection to the client is lost either from the client closing the connection the server
    #closing the connection or loss of the socket   
    def websocket_disconnect(self,event):
        print("Websocket Disconnected..")
        print("channel layer...",self.channel_layer)# channel name 
        print("channel name...",self.channel_name)# group name 
        
        async_to_sync(self.channel_layer.group_discard)(
            "programmers",
            self.channel_name
            
        )
        
        
# class MyAsyncConsumer(AsyncConsumer):
    
#     # this is handler is called when client initailly opns a
#     #connetions and is about to finish the webSocket handshake
#     async def websocket_connect(self,evet):
#         print("Websocket Connected...")
#         await self.send({
#              'type':"websocket.accept"
#          })
         
#     #this handler is called when data received from client     
#     async def websocket_receive(self,event):
#         print("message Received forn asyc..")
#         print(event['text'])
#         for i in range(50):
#             await self.send({
#                 'type':'websocket.send',
#                 'text':str(i)
#             })
#             await asyncio.sleep(1)
          
#     #this handler is called when either connection to the client is lost either from the client closing the connection the server
#     #closing the connection or loss of the socket   
#     async def websocket_disconnect(self,event):
#         print("Websocket Disconnected..")