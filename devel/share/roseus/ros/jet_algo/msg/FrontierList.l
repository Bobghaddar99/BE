;; Auto-generated. Do not edit!


(when (boundp 'jet_algo::FrontierList)
  (if (not (find-package "JET_ALGO"))
    (make-package "JET_ALGO"))
  (shadow 'FrontierList (find-package "JET_ALGO")))
(unless (find-package "JET_ALGO::FRONTIERLIST")
  (make-package "JET_ALGO::FRONTIERLIST"))

(in-package "ROS")
;;//! \htmlinclude FrontierList.msg.html


(defclass jet_algo::FrontierList
  :super ros::object
  :slots (_frontiers ))

(defmethod jet_algo::FrontierList
  (:init
   (&key
    ((:frontiers __frontiers) (let (r) (dotimes (i 0) (push (instance jet_algo::Frontier :init) r)) r))
    )
   (send-super :init)
   (setq _frontiers __frontiers)
   self)
  (:frontiers
   (&rest __frontiers)
   (if (keywordp (car __frontiers))
       (send* _frontiers __frontiers)
     (progn
       (if __frontiers (setq _frontiers (car __frontiers)))
       _frontiers)))
  (:serialization-length
   ()
   (+
    ;; jet_algo/Frontier[] _frontiers
    (apply #'+ (send-all _frontiers :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; jet_algo/Frontier[] _frontiers
     (write-long (length _frontiers) s)
     (dolist (elem _frontiers)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; jet_algo/Frontier[] _frontiers
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _frontiers (let (r) (dotimes (i n) (push (instance jet_algo::Frontier :init) r)) r))
     (dolist (elem- _frontiers)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get jet_algo::FrontierList :md5sum-) "8f27a97cf07f8421b3ea35c2336a4edc")
(setf (get jet_algo::FrontierList :datatype-) "jet_algo/FrontierList")
(setf (get jet_algo::FrontierList :definition-)
      "Frontier[] frontiers

================================================================================
MSG: jet_algo/Frontier
uint32 size
geometry_msgs/Point centroid

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

")



(provide :jet_algo/FrontierList "8f27a97cf07f8421b3ea35c2336a4edc")


