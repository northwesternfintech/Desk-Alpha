
CC=c++
CFLAGS=-g -Wall

TARGET=main

all: $(TARGET)

%: %.cpp
	$(CC) $(CFLAGS) -mmacosx-version-min=11.7 -std=c++11 $< -o $@ -lcurl 
	# -I/usr/local/Cellar//openssl@3/3.1.0/lib/ -L/usr/local/Cellar//openssl@3/3.1.0 -lcrypto

clean:
	$(RM) -rf $(BIN) *.dSYM-