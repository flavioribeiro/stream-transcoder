import sys
sys.path.insert(0, "/Library/Frameworks/GStreamer.framework/Versions/0.10/x86_64/lib/python2.7/site-packages/gst-0.10")
sys.path.insert(0, "/Library/Frameworks/GStreamer.framework/Versions/0.10/x86_64/lib/python2.7/site-packages")
import glib, gobject
import gst


def callback(bus, message):
    if message.type == gst.MESSAGE_ERROR:
        err, debug = message.parse_error()
        print "Error: %s" % err, debug
        loop.quit()
    elif message.type == gst.MESSAGE_EOS:
        print "Acabou-se!"
        loop.quit()

pipeline = gst.parse_launch("uridecodebin uri=%s name=src "
                            "src. ! queue ! tee name=audio  "
                            "src. ! queue ! tee name=video "
                            "audio. ! queue ! audioconvert ! faac ! m. "
                            "video. ! queue ! ffmpegcolorspace ! x264enc ! m. "
                            "mp4mux name=m ! filesink location=/tmp/foo.mp4 " % sys.argv[1])
bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", callback)
pipeline.set_state(gst.STATE_PLAYING)

gobject.threads_init()
loop = glib.MainLoop()
loop.run()

pipeline.set_state(gst.STATE_NULL)


