import datetime
from ExploreRecks import DroidBot


app_path = "ExploreRecks/input/samples/cn.fangchan.fanzan.apk"
device_serial = "######"    # Device serial number
output_dir = "ExploreRecks/output/utgs/"


def main():
    """
    the main function
    it starts a droidbot according to the arguments given in cmd line
    """
    start_time = datetime.datetime.now()
    print("***** start time：", start_time)
    try:
        droidbot = DroidBot(app_path=app_path,
                            device_serial=device_serial,
                            is_emulator=False,
                            output_dir=output_dir,
                            env_policy=None,
                            policy_name="red_packet_first",
                            random_input=False,
                            script_path=None,
                            event_count=-1,
                            event_interval=5,
                            timeout=-1,
                            keep_app=True,
                            keep_env=True,
                            cv_mode=False,
                            debug_mode=False,
                            profiling_method=None,
                            grant_perm=True)

        droidbot.start()
    except:
        droidbot.stop()
        import traceback
        traceback.print_exc()

    end_time = datetime.datetime.now()
    print("***** end time：", end_time)
    time = (end_time - start_time).seconds + (end_time - start_time).microseconds / 1000000
    print('time: ' + str(time) + 's')
    return


if __name__ == "__main__":
    main()
