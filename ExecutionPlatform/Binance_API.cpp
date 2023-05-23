#include "Binance_API.h"

#include <iostream>
#include <queue>
#include <stdexcept>
// #include <ctime>
#include <curl/curl.h>

#include <string>
#include <chrono>
#include <openssl/hmac.h>
#include <iomanip>
#include <sstream>
#include <map>

using namespace std;

// Constructor
executionPlatform::executionPlatform(string apiKey, string apiSecret, string baseURL) 
    : apiKey_(apiKey),
      apiSecret_(apiSecret),
      baseURL_("/api/v3"),
      internalID_(0)
    //   orderQueue_(orderQueue)
{ }


// size_t 
// executionPlatform::WriteCallback(void *contents, size_t size, size_t nmemb, void *userp){
//     ((string*)userp)->append((char*)contents, size * nmemb);
//     return size * nmemb;
// }


string 
executionPlatform::encryptWithHMAC(const char* key, const char* data) {
    unsigned char *result;
    static char res_hexstring[64];
    int result_len = 32;
    string signature;

    result = HMAC(EVP_sha256(), key, strlen((char *)key), const_cast<unsigned char *>(reinterpret_cast<const unsigned char*>(data)), strlen((char *)data), NULL, NULL);
  	for (int i = 0; i < result_len; i++) {
    	sprintf(&(res_hexstring[i * 2]), "%02x", result[i]);
  	}

  	for (int i = 0; i < 64; i++) {
  		signature += res_hexstring[i];
  	}

  	return signature;
}


string 
executionPlatform::getTimestamp() {
	long long ms_since_epoch = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
	return to_string(ms_since_epoch);
}


string 
executionPlatform::getSignature(string query) {
	string signature = executionPlatform::encryptWithHMAC(apiSecret_.c_str(), query.c_str());
	return "&signature=" + signature;
}


/* concatenate the query parameters to &<key>=<value> */
string 
executionPlatform::joinQueryParameters(const map<string,string> &parameters) {
	string queryString = "";
	for (auto it = parameters.cbegin(); it != parameters.cend(); ++it) {
        if (it == parameters.cbegin()) {
            queryString += it->first + '=' + it->second;
        }

        else {
            queryString += '&' + it->first + '=' + it->second;
        }
	}

	return queryString;
}


size_t 
executionPlatform::WriteCallback(char *contents, size_t size, size_t nmemb, void *userp) {
    gs_strLastResponse += (const char*)contents;
    gs_strLastResponse += '\n';
    return size * nmemb;
}


void 
executionPlatform::executeHTTPRequest(CURL *curl) {
	CURLcode res;
	gs_strLastResponse = "";
	/* Perform the request, res will get the return code */ 
	res = curl_easy_perform(curl);
	/* Check for errors */ 
	if(res != CURLE_OK)
	  fprintf(stderr, "curl_easy_perform() failed: %s\n",
	          curl_easy_strerror(res));
	cout << gs_strLastResponse << endl;
}


void
executionPlatform::sendPublicRequest(CURL *curl, string urlPath, map<string,string> &parameters) {

	string url = baseURL_ + urlPath + '?';
    if (!parameters.empty()) {
    	url += joinQueryParameters(parameters);
    }
    cout << "url:" << url << endl;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
	parameters.clear();
	executeHTTPRequest(curl);
}


void 
executionPlatform::sendSignedRequest(CURL *curl, string httpMethod, string urlPath, map<string,string> &parameters) {
	string url = baseURL_ + urlPath + '?';
	string queryString = "";
	string timeStamp = "timestamp=" + getTimestamp();
	if (!parameters.empty()) {
		string res = joinQueryParameters(parameters) + '&' + timeStamp;
		url += res;
		queryString += res; 
	}

	else {
		url += timeStamp;
		queryString += timeStamp;
	}

	string signature = getSignature(queryString);
	url += signature;
	queryString += signature;
	cout << "url:" << url << endl;

	if (httpMethod == "POST") {
		curl_easy_setopt(curl, CURLOPT_URL, (baseURL_ + urlPath).c_str());
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, queryString.c_str());
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
		parameters.clear();
		executeHTTPRequest(curl);
	}

    else if (httpMethod == "DELETE") {
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "DELETE");
		curl_easy_setopt(curl, CURLOPT_URL, (baseURL_ + urlPath).c_str());
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, queryString.c_str());
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
		parameters.clear();
		executeHTTPRequest(curl);
	}

	else {
		curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
		executeHTTPRequest(curl);
	}
}






string
executionPlatform::getBalance() {
    /*
    Inputs  : None
    Returns : CURL response string
    Errors  : None
    */

    CURL *curl;
	map<string,string> parameters;
	string queryString;

	curl_global_init(CURL_GLOBAL_ALL);

	curl = curl_easy_init();
	if(curl) {
        // Adding API key to header 
        struct curl_slist *chunk = NULL;
		chunk = curl_slist_append(chunk, ("X-MBX-APIKEY:" + apiKey_).c_str());
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
        string urlPath = baseURL_ + "/account";

        // Sending get request
        sendSignedRequest(curl, "GET", urlPath, parameters);
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
    return gs_strLastResponse;
}


string
executionPlatform::inspectOrder(string symbol, long *orderId) {
    /*
    Inputs  : symbol - asset symbol
              orderId - order ID in Binance Spot account
    Returns : CURL response string
        - returns specific order status if (long int) orderId is passed
        - returns all order statuses for a specific asset if NULL is passed as *orderID
    Errors  : 
    */ 
    CURL *curl;
	map<string,string> parameters;
	string queryString;

	curl_global_init(CURL_GLOBAL_ALL);

	curl = curl_easy_init();
	if(curl) {
        // Adding API key to header 
        struct curl_slist *chunk = NULL;
		chunk = curl_slist_append(chunk, ("X-MBX-APIKEY:" + apiKey_).c_str());
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);

        if (orderId== NULL) {
            string urlPath = baseURL_ + "/allOrders";
            parameters.insert({"symbol", symbol});
            // Sending get request
            sendSignedRequest(curl, "GET", urlPath, parameters);
            curl_easy_cleanup(curl);
        }
        else {
            string urlPath = baseURL_ + "/order";
            parameters.insert({
                {"symbol", symbol},
                {"orderID", to_string(*orderId)}});
            // Sending get request
            sendSignedRequest(curl, "GET", urlPath, parameters);
            curl_easy_cleanup(curl);
        }
    }
    curl_global_cleanup();
    return gs_strLastResponse;
} 


string
executionPlatform::cancelOrder(string symbol, long orderId) {
    /*
    Inputs  : symbol - asset symbol
              orderId - order ID in Binance Spot account
    Returns : CURL response string
    Errors  : 
    */
     CURL *curl;
    map<string,string> parameters;
	string queryString;

	curl_global_init(CURL_GLOBAL_ALL);

	curl = curl_easy_init();
	if(curl) {
        // Adding API key to header 
        struct curl_slist *chunk = NULL;
		chunk = curl_slist_append(chunk, ("X-MBX-APIKEY:" + apiKey_).c_str());
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
        string urlPath = baseURL_ + "/order";

        parameters.insert({
			{"symbol", symbol},
			{"orderID", to_string(orderId)}});

        // Sending get request
        sendSignedRequest(curl, "DELETE", urlPath, parameters);
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
    return gs_strLastResponse;
}


string
executionPlatform::changeOrder(long orderId, string symbol, string side, string type, string timeInForce, float amount, float price) {
    /*
    Inputs  : internalId - internally stored id in our executionPlatform class
              symbol - asset symbol
              side - "buy" or "sell"
              type - Enum: "MARKET" "LIMIT" "STOP_LOSS" "STOP_LOSS-LIMIT" "TAKE-PROFIT" "TAKE-PROFIT-LIMIT" "LIMIT_MAKER"
              timeInForce - Enum: "GTC", "IOC", "FOK"
              amount - order quantity in terms of the base asset
              price - Limit price for limit orders
                      Trigger price for stop-loss, stop-loss-limit, take-profit and take-profit-limit orders                 
    Returns : CURL response string
    Errors  : 
    */
    gs_strLastResponse = "";
    string res1 = cancelOrder(symbol, orderId);
    if (res1.compare("") != 0) {
        return "order cancellation failed";
    } 

    gs_strLastResponse = "";
    string res2 = placeOrder(internalID_, symbol, side, type, timeInForce, amount, price);
    if (res2.compare("") != 0) {
        return "order placement failed";
    }
    return res1 + res2;
}


string
executionPlatform::placeOrder(int internalId, string symbol, string side, string type, string timeInForce, float amount, float price) {   
    /*
    Inputs  : internalId - internally stored id in our executionPlatform class
              symbol - asset symbol
              side - "buy" or "sell"
              type - Enum: "MARKET" "LIMIT" "STOP_LOSS" "STOP_LOSS-LIMIT" "TAKE-PROFIT" "TAKE-PROFIT-LIMIT" "LIMIT_MAKER"
              timeInForce - Enum: "GTC", "IOC", "FOK"
              amount - order quantity in terms of the base asset
              price - Limit price for limit orders
                      Trigger price for stop-loss, stop-loss-limit, take-profit and take-profit-limit orders          
    Returns : CURL response string
    Errors  : 
    */
    CURL *curl;
    map<string,string> parameters;
	string queryString;

	curl_global_init(CURL_GLOBAL_ALL);

	curl = curl_easy_init();
	if(curl) {
        // Adding API key to header 
        struct curl_slist *chunk = NULL;
		chunk = curl_slist_append(chunk, ("X-MBX-APIKEY:" + apiKey_).c_str());
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
        string urlPath = baseURL_ + "/order";

        parameters.insert({
			{"symbol", symbol},
			{"side", side},
			{"type", type},
			{"timeInForce", timeInForce},
			{"quantity", to_string(amount)},
			{"price", to_string(price)}});

        // Sending get request
        sendSignedRequest(curl, "POST", urlPath, parameters);
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
    return gs_strLastResponse;
}   


int executionPlatform::retryOrders(){
    return 2;
}


void executionPlatform::run(){
    return;
}


/*
Order attributes:
{   'category' : 'place', 'change', 'cancel' (type=string),             | the category of the queue entry
    'timePlaced' : datetime object (type=datetime.datetime),            | the time the order was placed
    'retryTime' : timedelta object (type=datetime.timedelta),           | the maximum elapsed time the order can be in the queue before it is cancelled
    'internalID' : 12345, (type=int),                               ??? | the INTERNAL ID of the order, generated by the trading team. This is the ID that will be used to cancel or modify the order. it will be internally mapped to a txid.
    'txid' : 'OBCMZD-JIEE7-77TH3F', (type=string),                      | the transaction ID on the Kraken exchange
    'symbol' : 'XBTUSD', (type=string),                                 | the asset pair id or altname
    'side' : 'buy' or 'sell' (type=string),                             | the side of the order
    'type' : 'limit', 'market', etc. (type=string),                     | the type of the order
    'amount' : 1.0, (type=float),                                       | the amount of the order
    'price' : 100.0 (type=float) (should be None for market orders)     | the price of the order (only for limit place & limit modify orders)
}

type = Enum: "market", "limit", "stop-loss", "take-profit", "stop-loss-limit", "take-profit-limit", "settle-position"
*/
