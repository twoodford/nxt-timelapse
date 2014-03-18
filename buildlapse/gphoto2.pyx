cdef extern from "gphoto2/gphoto2-camera.h":
    ctypedef struct Camera:
        pass
    ctypedef struct GPContext:
        pass
    ctypedef struct CameraWidget:
        pass
    ctypedef void (* GPContextMessageFunc)  (GPContext *context, const char *text, void *data)
    ctypedef void (* GPContextErrorFunc)    (GPContext *context, const char *text, void *data)
    ctypedef struct CameraWidget:
        pass

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

    int gp_widget_ref(CameraWidget *widget)
    int gp_widget_unref(CameraWidget *widget)
    int gp_widget_get_child_by_label(CameraWidget *widget, const char *label, CameraWidget **child)
    int gp_widget_get_child_by_name(CameraWidget *widget, const char *label, CameraWidget **child)
    int gp_widget_get_name(CameraWidget *widget, const char **name)
    int gp_widget_set_name(CameraWidget *widget, const char *name)
    int gp_widget_get_label(CameraWidget *widget, const char **label)
    int gp_widget_count_choices(CameraWidget *widget)
    int gp_widget_get_choice(CameraWidget *widget, int choice_number, const char **choice)

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

    @property
    def root_widget(self):
        cdef CameraWidget *cwidget
        cdef int err = gp_camera_get_config(self._camera, &cwidget, self._context)
        if err!=GP_OK:
            raise Exception("gp_camera_get_config returned an error")
        ret = GPWidget()
        ret._gpinit(cwidget)
        return ret

    def __dealloc__(self): 
        gp_camera_unref(self._camera)
        gp_context_unref(self._context)

cdef class GPWidget(object):
    cdef CameraWidget *widg
    def __cinit__(self):
        pass

    cdef _gpinit(self, CameraWidget *inner):
        self.widg = inner
        gp_widget_ref(self.widg)

    @property
    def name(self):
        cdef const char *ret
        cdef int err = gp_widget_get_name(self.widg, &ret)
        if err != GP_OK:
            raise Exception("gp_widget_get_name returned an error")
        return ret

    @name.setter
    def name(self, value):
        cdef const char *val = value
        if gp_widget_set_name(self.widg, val) != GP_OK:
            raise Exception("gp_widget_set_name returned an error")

    @property
    def label(self):
        cdef const char *ret
        cdef int err = gp_widget_get_label(self.widg, &ret)
        if err != GP_OK:
            raise Exception("gp_widget_get_label returned an error")
        return ret

    @property
    def choices(self):
        cdef int numchoices = gp_widget_count_choices(self.widg)
        cdef const char *choice
        ret = []
        cdef int i
        for i in range(0, numchoices):
            if gp_widget_get_choice(self.widg, i, &choice) != GP_OK:
                raise Exception("gp_widget_get_choice() failed")
            ret.append(choice)
        return ret

    def child_by_label(self, name):
        cdef CameraWidget *ret
        encname = name.encode()
        if gp_widget_get_child_by_label(self.widg, encname, &ret) != GP_OK:
            raise Exception("gp_widget_get_child_by_label() failed")
        pyret = GPWidget()
        pyret._gpinit(ret)
        return pyret
    
    def child_by_name(self, name):
        cdef CameraWidget *ret
        encname = name.encode()
        if gp_widget_get_child_by_name(self.widg, encname, &ret) != GP_OK:
            raise Exception("gp_widget_get_child_by_name() failed")
        pyret = GPWidget()
        pyret._gpinit(ret)
        return pyret

    def __dealloc__(self):
        gp_widget_unref(self.widg)

def test():
    teth = GPTether()
    teth.connect_camera()
    #teth.trigger_capture()
    root = teth.root_widget
    print(root.name)
    print(root.label)
    shutterspeed = root.child_by_name("capturesettings").child_by_name("shutterspeed2")
    print(shutterspeed.name)
    print(shutterspeed.label)
    print(shutterspeed.choices)
