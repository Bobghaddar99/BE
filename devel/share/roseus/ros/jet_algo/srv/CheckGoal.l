;; Auto-generated. Do not edit!


(when (boundp 'jet_algo::CheckGoal)
  (if (not (find-package "JET_ALGO"))
    (make-package "JET_ALGO"))
  (shadow 'CheckGoal (find-package "JET_ALGO")))
(unless (find-package "JET_ALGO::CHECKGOAL")
  (make-package "JET_ALGO::CHECKGOAL"))
(unless (find-package "JET_ALGO::CHECKGOALREQUEST")
  (make-package "JET_ALGO::CHECKGOALREQUEST"))
(unless (find-package "JET_ALGO::CHECKGOALRESPONSE")
  (make-package "JET_ALGO::CHECKGOALRESPONSE"))

(in-package "ROS")

(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))




(defclass jet_algo::CheckGoalRequest
  :super ros::object
  :slots (_goal ))

(defmethod jet_algo::CheckGoalRequest
  (:init
   (&key
    ((:goal __goal) (instance geometry_msgs::PoseStamped :init))
    )
   (send-super :init)
   (setq _goal __goal)
   self)
  (:goal
   (&rest __goal)
   (if (keywordp (car __goal))
       (send* _goal __goal)
     (progn
       (if __goal (setq _goal (car __goal)))
       _goal)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/PoseStamped _goal
    (send _goal :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/PoseStamped _goal
       (send _goal :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/PoseStamped _goal
     (send _goal :deserialize buf ptr-) (incf ptr- (send _goal :serialization-length))
   ;;
   self)
  )

(defclass jet_algo::CheckGoalResponse
  :super ros::object
  :slots (_is_applicable ))

(defmethod jet_algo::CheckGoalResponse
  (:init
   (&key
    ((:is_applicable __is_applicable) nil)
    )
   (send-super :init)
   (setq _is_applicable __is_applicable)
   self)
  (:is_applicable
   (&optional __is_applicable)
   (if __is_applicable (setq _is_applicable __is_applicable)) _is_applicable)
  (:serialization-length
   ()
   (+
    ;; bool _is_applicable
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _is_applicable
       (if _is_applicable (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _is_applicable
     (setq _is_applicable (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass jet_algo::CheckGoal
  :super ros::object
  :slots ())

(setf (get jet_algo::CheckGoal :md5sum-) "547d92c6b43afde2ab954b07f001fe33")
(setf (get jet_algo::CheckGoal :datatype-) "jet_algo/CheckGoal")
(setf (get jet_algo::CheckGoal :request) jet_algo::CheckGoalRequest)
(setf (get jet_algo::CheckGoal :response) jet_algo::CheckGoalResponse)

(defmethod jet_algo::CheckGoalRequest
  (:response () (instance jet_algo::CheckGoalResponse :init)))

(setf (get jet_algo::CheckGoalRequest :md5sum-) "547d92c6b43afde2ab954b07f001fe33")
(setf (get jet_algo::CheckGoalRequest :datatype-) "jet_algo/CheckGoalRequest")
(setf (get jet_algo::CheckGoalRequest :definition-)
      "geometry_msgs/PoseStamped goal

================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
---
bool is_applicable

")

(setf (get jet_algo::CheckGoalResponse :md5sum-) "547d92c6b43afde2ab954b07f001fe33")
(setf (get jet_algo::CheckGoalResponse :datatype-) "jet_algo/CheckGoalResponse")
(setf (get jet_algo::CheckGoalResponse :definition-)
      "geometry_msgs/PoseStamped goal

================================================================================
MSG: geometry_msgs/PoseStamped
# A Pose with reference coordinate frame and timestamp
Header header
Pose pose

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
---
bool is_applicable

")



(provide :jet_algo/CheckGoal "547d92c6b43afde2ab954b07f001fe33")


