# C type definitions from the GPhoto2 library

cdef extern from "gphoto2/gphoto2-camera.h":
    ctypedef struct Camera:
        pass
    ctypedef struct GPContext:
        pass
    ctypedef struct CameraWidget:
        pass
    ctypedef struct CameraFilePath:
        char name[128]
        char folder[128]
    ctypedef void (* GPContextMessageFunc)  (GPContext *context, const char *text, void *data)
    ctypedef void (* GPContextErrorFunc)    (GPContext *context, const char *text, void *data)
    ctypedef struct CameraWidget:
        pass
    ctypedef enum CameraEventType:
        GP_EVENT_UNKNOWN, GP_EVENT_TIMEOUT, GP_EVENT_FILE_ADDED, GP_EVENT_FOLDER_ADDED, GP_EVENT_CAPTURE_COMPLETE
    ctypedef enum CameraCaptureType:
        GP_CAPTURE_IMAGE, GP_CAPTURE_MOVE, GP_CAPTURE_SOUND

    cdef int GP_OK

    int gp_camera_new (Camera **camera)
    int gp_camera_init (Camera *camera, GPContext *context)
    int gp_camera_trigger_capture(Camera *camera, GPContext *context)
    int gp_camera_capture(Camera *camera, CameraCaptureType type, CameraFilePath *path, \
            GPContext *context);
    int gp_camera_get_config(Camera *camera, CameraWidget **window, GPContext *context)
    int gp_camera_wait_for_event(Camera *camera, int timeout, CameraEventType *eventtype, \
            void **eventdata, GPContext *context)
    int gp_camera_file_get_info(Camera *camera, const char *folder, 
                 const char *file, CameraFileInfo *info,
                 GPContext *context) 
    int gp_camera_file_get(Camera *camera, const char *folder, const char *file, \
            CameraFileType type, CameraFile *camera_file, GPContext *ctx)
    int gp_camera_unref (Camera *camera)
    
    GPContext *gp_context_new ()
    void gp_context_set_error_func(GPContext *text, GPContextErrorFunc func, void *data)
    void gp_context_set_message_func(GPContext *text, GPContextMessageFunc func, void *data)
    int gp_context_unref (GPContext *context)

    int gp_widget_ref(CameraWidget *widget)
    int gp_widget_unref(CameraWidget *widget)
    int gp_widget_get_child_by_label(CameraWidget *widget, const char *label, CameraWidget **child)
    int gp_widget_get_child_by_name(CameraWidget *widget, const char *label, CameraWidget **child)
    int gp_widget_get_name(CameraWidget *widget, const char **name)
    int gp_widget_set_name(CameraWidget *widget, const char *name)
    int gp_widget_get_label(CameraWidget *widget, const char **label)
    int gp_widget_count_choices(CameraWidget *widget)
    int gp_widget_get_choice(CameraWidget *widget, int choice_number, const char **choice)
    int gp_widget_get_value(CameraWidget *widget, void *value)
    int gp_widget_set_value(CameraWidget *widget, const void *value)

cdef extern from "gp2util.h":
    int set_config_action (GPContext *context, Camera *camera, const char *name, const char *value) 

cdef extern from "gphoto2/gphoto2-port-result.h":
    cdef int GP_ERROR
    cdef int GP_ERROR_BAD_PARAMETERS
    cdef int GP_ERROR_NO_MEMORY
    cdef int GP_ERROR_TIMEOUT
    cdef int GP_ERROR_NOT_SUPPORTED

cdef extern from "stdint.h":
    # Need these for CameraFileInfoFile type
    ctypedef unsigned long int uint64_t
    ctypedef unsigned int uint32_t

cdef extern from "gphoto2/gphoto2-filesys.h":
    ctypedef enum CameraFileStatus:
        GP_FILE_STATUS_DOWNLOADED, GP_FILE_STATUS_NOT_DOWNLOADED

    ctypedef struct CameraFileInfoFile:
        CameraFileStatus status
        uint64_t size
        char type[64]
        uint32_t width
        uint32_t height

    ctypedef struct CameraFileInfo:
        CameraFileInfoFile file

cdef extern from "gphoto2/gphoto2-file.h":
    int gp_file_new_from_fd(CameraFile **file, int fd)

    ctypedef struct CameraFile:
        pass

    # Note: use the NORMAL type instead of RAW on modern DSLRs (see original header)
    ctypedef enum CameraFileType:
        GP_FILE_TYPE_PREVIEW, GP_FILE_TYPE_NORMAL, GP_FILE_TYPE_RAW, \
                GP_FILE_TYPE_AUDIO, GP_FILE_TYPE_EXIF, GP_FILE_TYPE_METADATA

