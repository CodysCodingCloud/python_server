import asyncio

host = '127.0.0.1'
port = 8080
async def handle_request(reader, writer):
    request = (await reader.read(1000)).decode("utf-8")
    
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, world"
    writer.write(response.encode("utf-8"))
    await writer.drain()
    
    writer.close()

async def main():
    loop = asyncio.get_event_loop()
    server = loop.create_server(handle_request, host, port)
    # server = await asyncio.start_server(
    #     handle_request, host, port
    # )
    print("Server is listening for requests...")
    print("server", server)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())