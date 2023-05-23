#pragma once

#include <iostream>
#include <queue>
#include <stdexcept>
#include <ctime>
#include <curl/curl.h>

#include <chrono>
#include <openssl/hmac.h>
#include <iomanip>
#include <sstream>
#include <map>

using namespace std;

class executionPlatform {

public:

    // Constructor
    executionPlatform(string apiKey, string apiSecret, string baseURL);

    // Helpers
    string encryptWithHMAC(const char* key, const char* data);
    string getTimestamp();
    string getSignature(string query);
    string joinQueryParameters(const map<string,string> &parameters);
    static size_t WriteCallback(char *contents, size_t size, size_t nmemb, void *userp);
    void executeHTTPRequest(CURL *curl);
    void sendPublicRequest(CURL *curl, string urlPath, map<string,string> &parameters);
    void sendSignedRequest(CURL *curl, string httpMethod, string urlPath, map<string,string> &parameters);

    // API functions
    string getBalance();
    string inspectOrder(string symbol, long *orderId);
    string cancelOrder(string symbol, long orderId);
    string changeOrder(long orderId, string symbol, string side, string type, string timeInForce, float amount, float price);
    string placeOrder(int internalID, string symbol, string side, string type, string timeInForce, float amount, float price);
    int retryOrders();
    void run();


private:   
    string apiKey_;
    string apiSecret_;
    static string gs_strLastResponse;
    string baseURL_;
    int internalID_;
};


