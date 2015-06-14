import fitbit
import ConfigParser
from datetime import datetime, date, time
import pickle as pkl

dt = datetime.now()
today_midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
today_six_am = dt.replace(hour=6, minute=0, second=0, microsecond=0)

try:
    entire_log = pkl.load(open('/home/pi/sentinel/sleep_full_log.p', "rb"))
    summary_log = pkl.load(open('/home/pi/sentinel/sleep_summary.p', "rb"))
except:
    entire_log = []
    summary_log = []
#If we are between midnight and 6 AM today, log all sleeping data and
#sleeping summary into a log file
if dt > today_midnight and dt < today_six_am:
    parser = ConfigParser.SafeConfigParser()
    parser.read('/etc/sentinel/sentinel_configure.cfg')
    consumer_key = parser.get('FITBIT Parameters', 'C_KEY')
    consumer_secret = parser.get('FITBIT Parameters', 'C_SECRET')
    user_key = parser.get('FITBIT Parameters', 'U_KEY')
    user_secret = parser.get('FITBIT Parameters', 'U_SECRET')
    authd_client = fitbit.Fitbit(consumer_key, consumer_secret, resource_owner_key=user_key, resource_owner_secret=user_secret)

    full = authd_client.sleep(date=dt)
    summary = authd_client.sleep(date=dt)[u'summary'][u'totalMinutesAsleep']

    entire_log.append(full)
    summary_log.append(summary)

    pkl.dump(entire_log, open('/home/pi/sentinel/sleep_full_log.p', "wb"))
    pkl.dump(summary_log, open('/home/pi/sentinel/sleep_summary.p', "wb"))
