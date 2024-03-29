#include <assert.h>
#include <stdbool.h>
#include <stdint.h>

uint16_t calculate(const uint8_t *data, size_t size) {
    uint32_t sum = 0;
    while (size > 1) {
        sum += *((const uint16_t*)(data));
        data += 2;
        size -= 2;
    }
    if (size > 0)
        sum = sum + *(data);
    while (sum >> 16)
        sum = (sum & 0xFFFF) + (sum >> 16);
    return ~((uint16_t)(sum));
}

bool verify(const uint8_t *data, size_t size, uint16_t checksum) {
    uint32_t sum = 0;
    while (size > 1) {
        sum += *((const uint16_t*)(data));
        data += 2;
        size -= 2;
    }
    if (size > 0)
        sum = sum + *(data);
    while (sum >> 16)
        sum = (sum & 0xFFFF) + (sum >> 16);
    sum += checksum;
    return (sum == 0xFFFF);
}

void test1() {
    uint8_t data[] = {0, 1, 2, 3, 4, 5};
    uint16_t checksum = calculate(data, sizeof(data));
    assert(verify(data, sizeof(data), checksum)); // Passed
}

void test2() {
    uint8_t data[] = {100, 200, 150, 250, 50};
    uint16_t checksum = calculate(data, sizeof(data));
    assert(verify(data, sizeof(data), checksum)); // Passed
}

void test3() {
    uint8_t data[] = {'a', 'b', 'c', 'd', 'e', 'f'};
    uint16_t checksum = calculate(data, sizeof(data));
    assert(verify(data, sizeof(data), checksum)); // Passed
}

void test4() {
    uint8_t data1[] = {'a', 'b', 'c'};
    uint16_t checksum = calculate(data1, sizeof(data1));
    uint8_t data2[] = {'x', 'y', 'z'};
    assert(verify(data2, sizeof(data2), checksum)); // Failed
}

int main() {
    test1();
    test2();
    test3();
    test4();
    return 0;
}
