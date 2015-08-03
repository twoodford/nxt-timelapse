import os
import time
from buildlapse.libgphoto2 cimport *
from cython.operator cimport dereference

cdef void error_func (GPContext *context, const char *text, void *data):
    print("libghoto2 error: "+text.decode())

cdef void message_func (GPContext *context, const char *text, void *data):
    print("libgphoto2: "+text.decode())

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

    def capture_and_download(self, outfile):
        cdef CameraFilePath cpf
        cdef int outfhandle = os.open(outfile, os.O_WRONLY|os.O_CREAT)
        cdef int ret = gp_camera_capture(self._camera, GP_CAPTURE_IMAGE, &cpf, self._context)
        if ret != GP_OK:
            print("libgphoto2: Error during capture")
        else:
            self._download_file(cpf, outfhandle)

    # timeout is in milliseconds
    def handle_event(self, timeout):
        cdef CameraEventType evtypev = GP_EVENT_UNKNOWN
        cdef CameraEventType *evtype = &evtypev
        cdef void *data
        cdef int result = gp_camera_wait_for_event(self._camera, timeout, evtype, \
                &data, self._context)
        if result == GP_ERROR_NOT_SUPPORTED:
            time.sleep(timeout)
            return
        cdef CameraFilePath *path = <CameraFilePath *> data
        if result != GP_OK:
            raise Exception("Couldn't handle event (error "+str(result)+")")
        if dereference(evtype) == GP_EVENT_FOLDER_ADDED:
            print("libgphoto2: folder added, name="+path.name)
        elif dereference(evtype) == GP_EVENT_FILE_ADDED:
            print("libgphoto2: File added")
            # Currently, use the original camera file name for download
            self._download_file(dereference(path), \
                    os.open(path.name.decode(), os.O_WRONLY|os.O_CREAT))
        elif dereference(evtype) == GP_EVENT_CAPTURE_COMPLETE:
            print("libgphoto2: Capture complete")
        elif dereference(evtype) == GP_EVENT_UNKNOWN:
            print("libgphoto2: Unknown event type")

    cdef _download_file(self, CameraFilePath path, int outfd):
        print("Downloading file at "+path.folder.decode()+"/"+path.name.decode())
        cdef CameraFileInfo info
        gp_camera_file_get_info(self._camera, path.folder, path.name, &info, self._context)
        if info.file.status == GP_FILE_STATUS_DOWNLOADED:
            print("libgphoto2: File already downloaded")
            return
        cdef CameraFile *dstfile
        if gp_file_new_from_fd(&dstfile, outfd) != GP_OK:
            raise Exception("libgphoto2: Couldn't convert file descriptor to gphoto2 file")
        if gp_camera_file_get(self._camera, path.folder, path.name, GP_FILE_TYPE_NORMAL, \
                dstfile, self._context) != GP_OK:
            raise Exception("libgphoto2: Couldn't transfer file from camera")

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

    @property
    def value(self):
        # TODO check type (gp_widget_get_type(), if type==GP_WIDGET_RADIO or MENU)
        cdef const char *value = None # Need to make this more general
        gp_widget_get_value(self.widg, &value)
        return value

    @value.setter
    def value(self, nval):
        pass
        #cdef char *value = str(nval)
        #if set_config_action(self._context, self._camera, path, value) != GP_OK:
        #    raise Exception("set_config_action() failed")


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
    #teth.capture_and_download("test.jpg")
    #teth.handle_event(2000)
    #teth.handle_event(2000)
    root = teth.root_widget
    print(root.name)
    print(root.label)
    shutterspeed = root.child_by_name("capturesettings").child_by_name("shutterspeed2")
    print(shutterspeed.name)
    print(shutterspeed.label)
    print("Shutterspeed choices: {}".format(shutterspeed.choices))
    print("Number of choices: {}".format(len(shutterspeed.choices)))
    print("Shutterspeed value: {}".format(shutterspeed.value))
