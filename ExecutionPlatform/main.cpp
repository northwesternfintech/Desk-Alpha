// c++ main.cpp -o main -lcurl 

#include <iostream>
#include <sstream>
#include <iomanip>
#include <queue>
#include <curl/curl.h>
#include <unordered_map>

#include "Binance_API.h"
#include "Binance_API.cpp"

using namespace std;

// static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp){
//     ((string*)userp)->append((char*)contents, size * nmemb);
//     return size * nmemb;
// }

// int main(){
//     CURL * curl = curl_easy_init();
//     CURLcode res;
//     string readBuffer;

//     string url = "https://gnu.terminalroot.com.br/ip.php";

//     if(curl) {
//         curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
//         curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
//         curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
//         res = curl_easy_perform(curl);
//         if (res != CURLE_OK) {
//             std::cout << "curl_easy_perform() failed:" << curl_easy_strerror(res) << "\n";
//         }
//         curl_easy_cleanup(curl);

//         std::cout << readBuffer << std::endl;
//     }

//     curl_global_cleanup();

//     return 0;
// }

int main() {
    executionPlatform binance("j1RZOhpZUf0vGduUnXG2ao1mrdPtLl8FkmEIrZkzQtJiT3k97bDYYpeinJSIvAS5", 
                                "qqgVs85Y20j6n1fa41Ap6VSyGqL5wP1xrVM7ZTkQhgijCuAUbZvxQup9jNbNcW7O",
                                "https://api.binance.com");

    // long long ms_since_epoch = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
	// string time = to_string(ms_since_epoch);
    // string time = binance.getTimestamp();

    // cout << time << endl;
    // cout << signature << endl;

    return 0;
}
