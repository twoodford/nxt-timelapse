cdef extern from "gphoto2/gphoto2-camera.h":
    ctypedef struct Camera:
        pass
    ctypedef struct GPContext:
        pass
    ctypedef struct CameraWidget:
        pass
    ctypedef void (* GPContextMessageFunc)  (GPContext *context, const char *text, void *data)
    ctypedef void (* GPContextErrorFunc)    (GPContext *context, const char *text, void *data)

    cdef int GP_OK

    int gp_camera_new (Camera **camera)
    int gp_camera_init (Camera *camera, GPContext *context)
    int gp_camera_trigger_capture(Camera *camera, GPContext *context)
    int gp_camera_get_config(Camera *camera, CameraWidget **window, GPContext *context)
    int gp_camera_unref (Camera *camera)
    
    GPContext *gp_context_new ()
    void gp_context_set_error_func(GPContext *text, GPContextErrorFunc func, void *data)
    void gp_context_set_message_func(GPContext *text, GPContextMessageFunc func, void *data)
    int gp_context_unref (GPContext *context)

cdef void error_func (GPContext *context, const char *text, void *data):
            print("Error!!!!")
            print(str(text))

cdef void message_func (GPContext *context, const char *text, void *data):
            print("Message!!!")
            print(str(text))

cdef class GPTether:
    cdef Camera *_camera
    cdef GPContext *_context

    def __cinit__(self):
        gp_camera_new(&self._camera)
        if self._camera is NULL:
            raise Exception("Failed to create new Camera")
        self._context = gp_context_new()
        if self._context is NULL:
            raise Exception("Couldn't create a Context")
        gp_context_set_error_func(self._context, error_func, NULL)
        gp_context_set_message_func(self._context, message_func, NULL)

    def connect_camera(self):
        cdef int ret = gp_camera_init(self._camera, self._context)
        if ret < GP_OK:
            raise Exception("No camera could be detected!")

    def trigger_capture(self):
        cdef int ret = gp_camera_trigger_capture(self._camera, self._context)
        if ret < GP_OK:
            raise Exception("Couldn't trigger a capture")

    def __dealloc__(self): 
        gp_camera_unref(self._camera)
        gp_context_unref(self._context)

def test():
    teth = GPTether()
    teth.connect_camera()
    teth.trigger_capture()
