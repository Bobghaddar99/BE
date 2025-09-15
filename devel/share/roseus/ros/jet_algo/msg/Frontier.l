;; Auto-generated. Do not edit!


(when (boundp 'jet_algo::Frontier)
  (if (not (find-package "JET_ALGO"))
    (make-package "JET_ALGO"))
  (shadow 'Frontier (find-package "JET_ALGO")))
(unless (find-package "JET_ALGO::FRONTIER")
  (make-package "JET_ALGO::FRONTIER"))

(in-package "ROS")
;;//! \htmlinclude Frontier.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass jet_algo::Frontier
  :super ros::object
  :slots (_size _centroid ))

(defmethod jet_algo::Frontier
  (:init
   (&key
    ((:size __size) 0)
    ((:centroid __centroid) (instance geometry_msgs::Point :init))
    )
   (send-super :init)
   (setq _size (round __size))
   (setq _centroid __centroid)
   self)
  (:size
   (&optional __size)
   (if __size (setq _size __size)) _size)
  (:centroid
   (&rest __centroid)
   (if (keywordp (car __centroid))
       (send* _centroid __centroid)
     (progn
       (if __centroid (setq _centroid (car __centroid)))
       _centroid)))
  (:serialization-length
   ()
   (+
    ;; uint32 _size
    4
    ;; geometry_msgs/Point _centroid
    (send _centroid :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _size
       (write-long _size s)
     ;; geometry_msgs/Point _centroid
       (send _centroid :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _size
     (setq _size (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; geometry_msgs/Point _centroid
     (send _centroid :deserialize buf ptr-) (incf ptr- (send _centroid :serialization-length))
   ;;
   self)
  )

(setf (get jet_algo::Frontier :md5sum-) "02475197d3519817f561b4e34a7be18f")
(setf (get jet_algo::Frontier :datatype-) "jet_algo/Frontier")
(setf (get jet_algo::Frontier :definition-)
      "uint32 size
geometry_msgs/Point centroid

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

")



(provide :jet_algo/Frontier "02475197d3519817f561b4e34a7be18f")


