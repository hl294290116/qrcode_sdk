添加事件请按顺序添加事件类型和id
下面是已经使用的事件类型id
新增加事件，对应的event_id 不能和以前一样

参考activity_sdk/include/AibeeActivity.hpp

enum class ActivityType {
    fall,               // event_id -> 0
    fight,              // event_id -> 1
    cellphone_using,    // event_id -> 2
    screen_photo_taking,    // event_id -> 3
    screen_photo_taking_pose2d,    // event_id -> 4
};


事件类型记录

fall,               // evnet_id -> 0   跌倒事件
fight,              // event_id -> 1   打架事件
cellphone_using,    // event_id -> 2   手机使用事件
screen_photo_taking,    // event_id -> 3 手机拍屏事件
screen_photo_taking_pose2d,    // event_id -> 4 带pose的手机拍屏手机拍屏事件


