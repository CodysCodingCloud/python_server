import asyncio

host = '127.0.0.1'
port = 8080

response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, world"


class MYPROTOCOL(asyncio.Protocol):
    def __init__(self):
        self.buffer = b''
    def connection_made(self,transport):
        print(f">>>>>>>>>>>>>>>>>>>>\nConnection made from {transport.get_extra_info('peername')}")
        self.transport = transport
    def data_received(self, data):
        self.buffer+=data
        print(f'received {data}')
        if b'\r\n\r\n' in self.buffer:
            header, self.buffer = self.buffer.split(b'\r\n\r\n',1)
            start_line, *fields = header.decode('utf-8').split("\r\n")
            method, path, protocol = start_line.split(' ')

            header_fields={line.split(': ')[0]:line.split(': ')[1] for line in fields}
            if "Content-Length" in header_fields:
                print("Content-Length", header_fields["Content-Length"])
                if int(header_fields["Content-Length"]) != len(self.buffer):
                    print("buffer length short a bit lets get more data")
                    return
            self.transport.write(response.encode('utf-8'))
            self.transport.write_eof()
            print('sent my response')
            self.transport.close()
    def eof_received(self):
        print("eof received")
    def connection_lost(self, exc):
        print(f"connection closed {exc}")
async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(MYPROTOCOL, host, port)
    print("Server is listening for requests...")
    print("server", server)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())