import unittest

import calculate_taxi_fare


# メモ
# 10km/h = 166.666666.... <= 166.7m/m
# 10km/h = 2.7777777.... <= 2.8m/s

class CalculateTest(unittest.TestCase):
    def test_case_1(self):
        # Case 1
        # 総走行距離 1052m
        # expect: 410
        drive_logs = []
        with open('test_case/test_case_1.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(410, ride_fee)

    def test_case_2(self):
        # Case 2
        # 総走行距離 1053m
        # 初乗り 410 + 80
        # expect: 490
        drive_logs = []
        with open('test_case/test_case_2.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(490, ride_fee)

    def test_case_3(self):
        # Case 3
        # 総低速運転時間 89.999s -> 低速課金なし
        # 1052m未満 -> 初乗り料金
        # expect: 410
        drive_logs = []
        with open('test_case/test_case_3.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(410, ride_fee)

    def test_case_4(self):
        # Case 4
        # 低速運転 90s
        # 低速運転料金 = 90//90 * 80 = 80
        # 総走行距離 < 1052より初乗り = 410
        # expect: 490
        drive_logs = []
        with open('test_case/test_case_4.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(490, ride_fee)

    def test_case_5(self):
        # Case 5
        # 21:59:59.999 0.0 ~ 22:01:00.000
        # 総走行距離 842m -> 初乗り 410
        # expect: 410
        drive_logs = []
        with open('test_case/test_case_5.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(410, ride_fee)

    def test_case_6(self):
        # Case 6
        # 22:00:00.000 0.0 ~ 22:01:00.000
        # 深夜補正 842 * 1.25 = 1052.5 > 1052m　より初乗り 410 + 80
        # expect: 490
        drive_logs = []
        with open('test_case/test_case_6.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(490, ride_fee)

    def test_case_7(self):
        # Case 7
        # 04:59:00.000 ~ 04:59:59.999
        # 総走行距離 842m
        # 深夜補正がかかり 842 * 1.25 = 1052.5m >= 1052 より初乗り410 + 80
        # expect: 490
        drive_logs = []
        with open('test_case/test_case_7.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(490, ride_fee)

    def test_case_8(self):
        # Case 8
        # 04:59:59.999 ~ 05:00:00.000
        # 総走行距離 842
        # 終端が05:00のため深夜料金にならず初乗りのみ
        # expect: 410
        drive_logs = []
        with open('test_case/test_case_8.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(410, ride_fee)

    def test_case_9(self):
        # Case 9
        # 24:00以降も計算できることを検証
        # Case 7の24時間後パターン
        # 28:59:00.000 ~ 28:59:59.999
        # 総走行距離 842m
        # 深夜補正がかかり 842 * 1.25 = 1052.5m >= 1052 より初乗り410 + 80
        # expect: 490
        drive_logs = []
        with open('test_case/test_case_9.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(490, ride_fee)

    def test_case_10(self):
        # Case 10
        # 24:00以降も計算できることを検証
        # Case 8 の24時間後パターン
        # 28:59:59.999 ~ 28:00:00.000
        # 総走行距離 842
        # 終端が05:00のため深夜料金にならず初乗りのみ
        # expect: 410
        drive_logs = []
        with open('test_case/test_case_10.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(410, ride_fee)

    def test_case_11(self):
        # Case 11
        # 深夜 22:00 ~ 22:08
        # 総走行距離 27/10 * 8m * 60 = 1296m => 1296 * 1.25 = 1620
        # 総低速運転時間 420s
        # 距離料金 (1620 - 1052)/90 = 2.32.. = 3 => 3 * 80 + 410 = 650
        # 低速料金 420//90 => 80 * 4 * 1.25 = 400
        # expect: 1050
        drive_logs = []
        with open('test_case/test_case_11.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(1050, ride_fee)

    def test_case_12(self):
        # Case 12
        # 05:00:00 ~ 21:59:50
        # 毎10秒 30m
        # expect 62090
        drive_logs = []
        with open('test_case/test_case_12.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(62090, ride_fee)

    def test_case_13(self):
        # Case 13
        # 00:00:00 ~ 09:59:50
        # 毎10秒 30m
        # expect: 32010
        drive_logs = []
        with open('test_case/test_case_13.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(41130, ride_fee)

    def test_case_14(self):
        # Case 14
        # 10:00:00 ~ 10:59:50 30m
        # 11:00:00 ~ 11:59:50 10m
        # expect: 32010
        drive_logs = []
        with open('test_case/test_case_14.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    drive_logs.append(line.replace('\n', ''))
        ride_fee = calculate_taxi_fare.calculate_taxi_fare(drive_logs)
        self.assertEqual(8170, ride_fee)
