#include <cstdlib>
#include <cstdint>
#include <ctime>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <cassert>
#include <vector>
#include <cstdint>

//CRC-16/CCITT-FALSE
template <typename T>
uint16_t crc(const T*data, size_t len)
{
    uint16_t res = 0xFFFF;
    while (len--) {
        res ^= *data++ << 8;
        for (size_t i = 0; i < 8; i++)
            res = res & 0x8000 ? (res << 1) ^ 0x1021 : res << 1;
    }
    return res;
}

void straight_tests() {
    assert(crc<char>("abc", 3) == 20810);
    assert(crc<char>("Hello, World!", 13) == 26586);
    assert(crc<char>("xyz", 3) == 53289);
}

void inverse_tests() {
    assert(crc<char>("abc", 3) != crc<char>("abd", 3));
    assert(crc<char>("", 0) != crc<char>("x", 1));
}

constexpr size_t packet_size = 5;

std::vector<uint8_t> get_packet(const std::vector<uint8_t> &data, size_t pos) {
    return {data.begin() + pos, data.begin() + pos + std::min(packet_size, data.size() - pos)};
}

void print_packet(const std::vector<uint8_t> &packet) {
    for (auto ch : packet) {
        std::cout << std::setw(2) << std::setfill('0') << std::hex << (ch & 0xFF);
    }
    std::cout << std::endl;
}

void mutate_packet(std::vector<uint8_t> &packet) {
    auto tmp = std::rand() % (3 * packet.size());
    if (tmp > packet.size())
        return;
    size_t idx = tmp % packet.size();
    uint8_t mask = 1 << (std::rand() % 7);
    packet[idx] ^= mask;
}

int main() {
    std::srand(std::time(0));
    straight_tests();
    inverse_tests();
    std::fstream input("test.txt");
    std::vector<uint8_t> data(std::istreambuf_iterator<char>(input), {});
    size_t pos = 0;
    do {
        auto packet = get_packet(data, pos);
        std::cout << "Original\n";
        print_packet(packet);
        auto original_hash = crc(packet.data(), packet.size());
        std::cout << "CRC\n";
        std::cout << std::hex << original_hash << std::endl;
        packet.push_back((original_hash & 0xFF00) >> 8);
        packet.push_back(original_hash & 0x00FF);
        std::cout << "Encoded\n";
        print_packet(packet);
        mutate_packet(packet);
        std::cout << "Mutated\n";
        print_packet(packet);
        uint16_t mutated_hash = 0;
        mutated_hash += packet[packet.size() - 2] << 8;
        mutated_hash += packet[packet.size() - 1];
        packet.resize(packet.size() - 2);
        if (crc(packet.data(), packet.size()) != mutated_hash)
            std::cout << "Invalid packet\n";
        pos += packet_size;
    } while (pos < data.size());
}
