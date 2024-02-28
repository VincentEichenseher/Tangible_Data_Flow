#ifndef UNTITLED1_PREDEFINED_MARKERS_H
#define UNTITLED1_PREDEFINED_MARKERS_H

#include <stdint-gcc.h>
#include <vector>

namespace proc::mkr
{
    std::vector<std::vector<uint8_t >> predefined_markers_4x4 =
            {
                    // 4x4_id_20
                    std::vector<uint8_t>
                            {
                                    1, 0, 1, 1,
                                    0, 1, 0, 0,
                                    0, 1, 0, 1,
                                    0, 0, 0, 1
                            },

                    // 4x4_id_40
                    std::vector<uint8_t>
                            {
                                    0, 0, 0, 1,
                                    0, 1, 0, 0,
                                    0, 1, 0, 0,
                                    1, 1, 1, 0
                            },

                    //  4x4_id_60
                    std::vector<uint8_t>
                            {
                                    0, 0, 1, 1,
                                    1, 1, 1, 1,
                                    1, 1, 0, 1,
                                    0, 1, 1, 1
                            },

                    // 4x4_id_80
                    std::vector<uint8_t>
                            {
                                    1, 1, 1, 1,
                                    1, 1, 0, 0,
                                    0, 0, 0, 0,
                                    0, 0, 1, 0
                            },

                    // 4x4_id_100
                    std::vector<uint8_t>
                            {
                                    0, 1, 0, 1,
                                    1, 0, 1, 1,
                                    1, 1, 1, 1,
                                    1, 0, 0, 0
                            },

                    // 4x4_id_120
                    std::vector<uint8_t>
                            {
                                    0, 0, 0, 1,
                                    0, 0, 1, 0,
                                    0, 0, 1, 0,
                                    1, 0, 1, 0
                            },

                    // 4x4_id_140
                    std::vector<uint8_t>
                            {
                                    0, 1, 1, 0,
                                    0, 1, 0, 0,
                                    0, 0, 0, 0,
                                    1, 1, 0, 0
                            },

                    // 4x4_id_160
                    std::vector<uint8_t>
                            {
                                    0, 1, 0, 1,
                                    0, 0, 1, 0,
                                    1, 1, 0, 0,
                                    1, 0, 0, 1
                            },
            };
}

#endif //UNTITLED1_PREDEFINED_MARKERS_H
