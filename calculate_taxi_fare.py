import math
import datetime
import sys


class RecordError(Exception):
    pass


def calculate_price(distance: float, time: float) -> int:
    '''距離と時間からそれぞれ運行料金を求め合算する。

    :param distance: float 距離(m)
    :param time: float 時間(ms)
    :return: 距離料金と時間料金の合計
    '''
    time_price = time // 90 * 80
    print(time, time_price)

    if distance <= 1052:
        distance_price = 410
    else:
        distance_price = 410 + math.ceil((distance - 1052)/237) * 80
    return int(time_price + distance_price)


def calculate_taxi_fare(drive_logs: list) -> int:
    '''タクシーの運行料金を計算する
    :param drive_logs:
    第一引数にhh:mm:ss.fff形式の走行時間、第二引数に有効数字少数第一位の走行距離を持つリストを含むリスト
    ex. [['10:00:00:00', 30.5],['10:00:01.000', 20.0]]

    :return: int: 計算されたタクシーの運行料金をint型で返す
    '''

    total_distance = 0  # 総走行距離
    total_low_speed_time = 0  # 総低速運転時間

    for i, log in enumerate(drive_logs):
        log_time, distance = log.split()
        time = log_time.split(':')
        h = int(time[0])
        h_mod24 = h % 24
        m = int(time[1])
        s = int(time[2].split('.')[0])
        ms = int(time[2].split('.')[1])
        if 0 > h or h > 99:
            raise RecordError('Value h is out of time range. should be between 0 and 99')

        if i == 0:  # 最初のログレコード
            time_ms = ((h * 3600 + m * 60 + s) * 1000 + ms)  # 時間をmsに変換
            time_dt = datetime.time(h_mod24, m, s, ms)  # 時刻をdatetime.time形式で比較できるよう変換

        elif i >= 1:  # ２つ目以降のログレコード
            input_time_ms = ((h * 3600 + m * 60 + s) * 1000 + ms)  # 時間をmsに変換
            input_time_dt = datetime.time(h_mod24, m, s, ms)  # 時刻をdatetime.time形式で比較できるよう変換

            #  平均速度km/hを計算
            input_distance = float(distance)
            ride_time = input_time_ms - time_ms
            avg_v = input_distance / float(ride_time)  # 単位 m/ms
            avg_v_km_per_h = (avg_v / 1000) / (10 ** (-3) / 60 / 60)  # 単位 km/h

            #  低速度運転時間を計算
            if avg_v_km_per_h <= 10:
                low_speed_time = ride_time  # 単位 ms
            else:
                low_speed_time = 0

            #  レコードの時間帯を確認
            # 00:00 ~ 4:59 or 22:00 ~ 23:59判定
            if datetime.time(0, 0, 0, 0) <= time_dt <= datetime.time(4, 59, 59, 999) \
                    and datetime.time(0, 0, 0, 0) <= input_time_dt <= datetime.time(4, 59, 59, 999) \
                    or datetime.time(22, 0, 0, 0) <= time_dt <= datetime.time(23, 59, 59, 999) \
                    and datetime.time(22, 0, 0, 0) <= input_time_dt <= datetime.time(23, 59, 59, 999):
                total_distance += input_distance * 10 * 1.25  # 距離を2.5割増, 単位 m
                total_low_speed_time += low_speed_time/1000 * 1.25  # 　時間を2.5割増, 単位 sec
            else:  # 通常時間帯
                total_distance += input_distance * 10  # 単位 m * 10（floatの桁ズレ対策）
                total_low_speed_time += low_speed_time/1000  # 単位 sec

            time_ms = input_time_ms  # 次のループのtime_ms
            time_dt = input_time_dt  # 次のループのtime_dt

    if total_distance <= 0:
        raise RecordError('Total distance is 0')
    return calculate_price(total_distance/10, total_low_speed_time)


if __name__ == '__main__':
    # 標準入力からドライブログを取得
    drive_logs = []
    while True:
        log = input()
        if log:
            drive_logs.append(log)
        else:
            break

    # ログが２行以上あることをチェック
    if len(drive_logs) < 2:
        raise RecordError('Drive record must contain more than two lines')
    print(type(drive_logs[0][1]))
    if float(drive_logs[0][1]) != 0.0:
        raise RecordError('The distance record should start from 0.0')

    print(drive_logs)
    print(calculate_taxi_fare(drive_logs))
    sys.exit(0)
