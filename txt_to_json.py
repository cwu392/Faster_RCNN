import json
import argparse
import pandas as pd

d = {0: 'h_bicycle_and_pedestrian_prohibited', 1: 'h_bus_and_truck_prohibited', 2: 'h_truck_bus_prohibited', 3: 'h_truck_prohibited', 4: 'p1', 5: 'p10', 6: 'p11', 7: 'p12', 8: 'p13', 9: 'p14', 10: 'p15', 11: 'p16', 12: 'p17', 13: 'p18', 14: 'p19', 15: 'p2', 16: 'p20', 17: 'p21', 18: 'p22', 19: 'p23', 20: 'p24', 21: 'p25', 22: 'p26', 23: 'p27', 24: 'p28', 25: 'p3', 26: 'p4', 27: 'p5', 28: 'p6', 29: 'p60', 30: 'p7', 31: 'p8', 32: 'p9', 33: 'pa10', 34: 'pa12', 35: 'pa13', 36: 'pa14', 37: 'pa8', 38: 'pb', 39: 'pc', 40: 'pg', 41: 'ph1.5', 42: 'ph2', 43: 'ph2.1', 44: 'ph2.2', 45: 'ph2.4', 46: 'ph2.5', 47: 'ph2.6', 48: 'ph2.8', 49: 'ph2.9', 50: 'ph3', 51: 'ph3.2', 52: 'ph3.3', 53: 'ph3.5', 54: 'ph3.8', 55: 'ph4', 56: 'ph4.0', 57: 'ph4.2', 58: 'ph4.3', 59: 'ph4.4', 60: 'ph4.5', 61: 'ph4.8', 62: 'ph5', 63: 'ph5.3', 64: 'ph5.5', 65: 'pl0', 66: 'pl10', 67: 'pl100', 68: 'pl110', 69: 'pl120', 70: 'pl15', 71: 'pl180', 72: 'pl20', 73: 'pl25', 74: 'pl3', 75: 'pl30', 76: 'pl35', 77: 'pl4', 78: 'pl40', 79: 'pl5', 80: 'pl50', 81: 'pl60', 82: 'pl65', 83: 'pl70', 84: 'pl80', 85: 'pl90', 86: 'pm1.5', 87: 'pm10', 88: 'pm13', 89: 'pm15', 90: 'pm2', 91: 'pm2.5', 92: 'pm20', 93: 'pm25', 94: 'pm30', 95: 'pm35', 96: 'pm40', 97: 'pm46', 98: 'pm49', 99: 'pm5', 100: 'pm50', 101: 'pm55', 102: 'pm8', 103: 'pn', 104: 'pn40', 105: 'pne', 106: 'pr10', 107: 'pr100', 108: 'pr20', 109: 'pr30', 110: 'pr40', 111: 'pr45', 112: 'pr50', 113: 'pr60', 114: 'pr70', 115: 'pr80', 116: 'ps', 117: 'pw2', 118: 'pw2.5', 119: 'pw3', 120: 'pw3.2', 121: 'pw3.5', 122: 'pw4', 123: 'pw4.2', 124: 'pw4.5'}

def txt_to_json(path_to_txt, output_path):
    frames_list = []
    file = pd.read_csv(path_to_txt)
    used = []
    for i in xrange(len(file)):
        if i in used:
            continue
        line = file.iloc[i]
        # line = line.strip().split(',')
        frame_num = line[0]
        score = line[6]
        if score > 0.5:
            f_dict = {'frame_number': str(frame_num), 'RoIs': ''}
            xmin, ymin, xmax, ymax = int(float(line[1])), int(float(line[2])), int(float(line[3])), int(float(line[4]))
            delta_x, delta_y = xmax - xmin, ymax - ymin
            xmin, ymin, delta_x, delta_y = str(xmin), str(ymin), str(delta_x), str(delta_y)
            rois_list = [[d.get(int(line[5])), xmin, ymin, delta_x, delta_y]]
            while i < len(file) - 1 and frame_num == file.iloc[i + 1][0] and file.iloc[i + 1][6] > 0.5:
                xmin, ymin = int(float(file.iloc[i + 1][1])), int(float(file.iloc[i + 1][2]))
                xmax, ymax = int(float(file.iloc[i + 1][3])), int(float(file.iloc[i + 1][4]))
                delta_x, delta_y = xmax - xmin, ymax - ymin
                xmin, ymin, delta_x, delta_y = str(xmin), str(ymin), str(delta_x), str(delta_y)
                rois_list.append([d.get(int(file.iloc[i + 1][5])), xmin, ymin, delta_x, delta_y])
                i += 1
                used.append(i)
            print rois_list
            if len(rois_list) > 0:
                RoIs = ''
                for l in rois_list:
                    RoIs += ','.join(l) + ';'
                f_dict['RoIs'] = RoIs
                print(f_dict)
            frames_list.append(f_dict)

    json_dict = {'output': {'frames': frames_list}}
    with open(output_path, 'w') as out_file:
        json.dump(json_dict, out_file, indent = 4)

    # frames_list = []
    # file = open(path_to_txt, 'rb')
    # used = []
    # for line in file:
    #     line = line.strip().split(',')
    #     frame_num = line[0]
    #     f_dict = {'frame_number': str(frame_num), 'RoIs': ''}
    #     xmin, ymin, xmax, ymax = int(float(line[1])), int(float(line[2])), int(float(line[3])), int(float(line[4]))
    #     delta_x, delta_y = xmax - xmin, ymax - ymin
    #     xmin, ymin, delta_x, delta_y = str(xmin), str(ymin), str(delta_x), str(delta_y)
    #     rois_list = [d.get(int(line[5])), xmin, ymin, delta_x, delta_y]

    #     if len(rois_list) > 0:
    #         f_dict['RoIs'] = ','.join(rois_list) + ';'
    #         print(f_dict)
    #     frames_list.append(f_dict)

    # json_dict = {'output': {'frames': frames_list}}
    # with open(output_path, 'w') as out_file:
    #     json.dump(json_dict, out_file, indent = 4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-json-file',
                        required = True,
                        type = str,
                        dest = "out_path")
    parser.add_argument('-i', '--input-txt-file',
                        required = True,
                        type = str,
                        dest = "in_path")

    args = parser.parse_args()
    txt_to_json(args.in_path, args.out_path)