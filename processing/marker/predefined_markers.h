#ifndef UNTITLED1_PREDEFINED_MARKERS_H
#define UNTITLED1_PREDEFINED_MARKERS_H

#include <stdint-gcc.h>
#include <vector>

namespace proc::mkr
{
    std::vector<std::vector<uint8_t >> predefined_markers_6x6 =
    {
        std::vector<uint8_t >
        {
            1, 1, 0, 0, 1, 1,
            1, 1, 0, 0, 1, 1,
            0, 1, 1, 0, 0, 1,
            0, 0, 1, 1, 1, 1,
            1, 0, 0, 1, 0, 1,
            1, 0, 0, 1, 1, 0
        },

        std::vector<uint8_t >
        {
            1, 0, 0, 1, 0, 1,
            0, 1, 0, 0, 1, 1,
            0, 1, 1, 0, 0, 1,
            1, 1, 1, 0, 0, 0,
            0, 1, 0, 1, 1, 1,
            0, 0, 0, 0, 1, 0
        }
    };

    std::vector<std::vector<uint8_t >> predefined_markers_4x4 =
            {
                    // brown
                    std::vector<uint8_t>
                            {
                                    1, 1, 0, 1,
                                    1, 1, 0, 0,
                                    1, 0, 0, 1,
                                    0, 1, 1, 1
                            },

                    // green
                    std::vector<uint8_t>
                            {
                                    0, 0, 0, 0,
                                    1, 1, 1, 1,
                                    0, 1, 1, 0,
                                    0, 0, 0, 1
                            },

                    // red
                    std::vector<uint8_t>
                            {
                                    1, 0, 1, 1,
                                    0, 1, 0, 0,
                                    0, 1, 0, 1,
                                    0, 0, 0, 1
                            },

                    // yellow
                    std::vector<uint8_t>
                            {
                                    0, 0, 0, 1,
                                    1, 1, 1, 0,
                                    1, 0, 1, 0,
                                    1, 0, 1, 1
                            },

                    // trash can
                    std::vector<uint8_t>
                            {
                                    1, 1, 0, 0,
                                    0, 1, 0, 0,
                                    0, 0, 0, 1,
                                    0, 0, 1, 1
                            },

                    // smiley face
                    std::vector<uint8_t>
                            {
                                    0, 1, 0, 1,
                                    1, 0, 0, 0,
                                    1, 0, 1, 1,
                                    1, 1, 0, 0
                            }
            };
}

#endif //UNTITLED1_PREDEFINED_MARKERS_H
