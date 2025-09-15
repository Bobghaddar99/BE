; Auto-generated. Do not edit!


(cl:in-package jet_algo-srv)


;//! \htmlinclude CheckGoal-request.msg.html

(cl:defclass <CheckGoal-request> (roslisp-msg-protocol:ros-message)
  ((goal
    :reader goal
    :initarg :goal
    :type geometry_msgs-msg:PoseStamped
    :initform (cl:make-instance 'geometry_msgs-msg:PoseStamped)))
)

(cl:defclass CheckGoal-request (<CheckGoal-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CheckGoal-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CheckGoal-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name jet_algo-srv:<CheckGoal-request> is deprecated: use jet_algo-srv:CheckGoal-request instead.")))

(cl:ensure-generic-function 'goal-val :lambda-list '(m))
(cl:defmethod goal-val ((m <CheckGoal-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader jet_algo-srv:goal-val is deprecated.  Use jet_algo-srv:goal instead.")
  (goal m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CheckGoal-request>) ostream)
  "Serializes a message object of type '<CheckGoal-request>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'goal) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CheckGoal-request>) istream)
  "Deserializes a message object of type '<CheckGoal-request>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'goal) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CheckGoal-request>)))
  "Returns string type for a service object of type '<CheckGoal-request>"
  "jet_algo/CheckGoalRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CheckGoal-request)))
  "Returns string type for a service object of type 'CheckGoal-request"
  "jet_algo/CheckGoalRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CheckGoal-request>)))
  "Returns md5sum for a message object of type '<CheckGoal-request>"
  "547d92c6b43afde2ab954b07f001fe33")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CheckGoal-request)))
  "Returns md5sum for a message object of type 'CheckGoal-request"
  "547d92c6b43afde2ab954b07f001fe33")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CheckGoal-request>)))
  "Returns full string definition for message of type '<CheckGoal-request>"
  (cl:format cl:nil "geometry_msgs/PoseStamped goal~%~%================================================================================~%MSG: geometry_msgs/PoseStamped~%# A Pose with reference coordinate frame and timestamp~%Header header~%Pose pose~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CheckGoal-request)))
  "Returns full string definition for message of type 'CheckGoal-request"
  (cl:format cl:nil "geometry_msgs/PoseStamped goal~%~%================================================================================~%MSG: geometry_msgs/PoseStamped~%# A Pose with reference coordinate frame and timestamp~%Header header~%Pose pose~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CheckGoal-request>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'goal))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CheckGoal-request>))
  "Converts a ROS message object to a list"
  (cl:list 'CheckGoal-request
    (cl:cons ':goal (goal msg))
))
;//! \htmlinclude CheckGoal-response.msg.html

(cl:defclass <CheckGoal-response> (roslisp-msg-protocol:ros-message)
  ((is_applicable
    :reader is_applicable
    :initarg :is_applicable
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass CheckGoal-response (<CheckGoal-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CheckGoal-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CheckGoal-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name jet_algo-srv:<CheckGoal-response> is deprecated: use jet_algo-srv:CheckGoal-response instead.")))

(cl:ensure-generic-function 'is_applicable-val :lambda-list '(m))
(cl:defmethod is_applicable-val ((m <CheckGoal-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader jet_algo-srv:is_applicable-val is deprecated.  Use jet_algo-srv:is_applicable instead.")
  (is_applicable m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CheckGoal-response>) ostream)
  "Serializes a message object of type '<CheckGoal-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'is_applicable) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CheckGoal-response>) istream)
  "Deserializes a message object of type '<CheckGoal-response>"
    (cl:setf (cl:slot-value msg 'is_applicable) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CheckGoal-response>)))
  "Returns string type for a service object of type '<CheckGoal-response>"
  "jet_algo/CheckGoalResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CheckGoal-response)))
  "Returns string type for a service object of type 'CheckGoal-response"
  "jet_algo/CheckGoalResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CheckGoal-response>)))
  "Returns md5sum for a message object of type '<CheckGoal-response>"
  "547d92c6b43afde2ab954b07f001fe33")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CheckGoal-response)))
  "Returns md5sum for a message object of type 'CheckGoal-response"
  "547d92c6b43afde2ab954b07f001fe33")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CheckGoal-response>)))
  "Returns full string definition for message of type '<CheckGoal-response>"
  (cl:format cl:nil "bool is_applicable~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CheckGoal-response)))
  "Returns full string definition for message of type 'CheckGoal-response"
  (cl:format cl:nil "bool is_applicable~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CheckGoal-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CheckGoal-response>))
  "Converts a ROS message object to a list"
  (cl:list 'CheckGoal-response
    (cl:cons ':is_applicable (is_applicable msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'CheckGoal)))
  'CheckGoal-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'CheckGoal)))
  'CheckGoal-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CheckGoal)))
  "Returns string type for a service object of type '<CheckGoal>"
  "jet_algo/CheckGoal")