import xml.etree.ElementTree as ET
import simplejson as json
import sys

annotation_file = sys.argv[1]
output_file_name = sys.argv[2]

tree = ET.parse(annotation_file)
root = tree.getroot()
print(root.tag)

for child in root:
	for grandchild in child:
		if grandchild.tag=="File":
			print(grandchild.text)

frameList = []

frameDict = {}
for child in root:
	for grandchild in child:
		if grandchild.tag=="File":
			filename = grandchild.text
		if grandchild.tag=="DetectedSigns":
			bboxstring = ""
			signIds = ""
			signClasses = ""
			for ggchild in grandchild:
				if ggchild.tag=="DetectedSign":
					bboxstring+=ggchild[0].text + ","
					bboxstring+=ggchild[1].text + ","
					bboxstring+=ggchild[2].text + ","

					for i in range(3):
						bboxstring += ggchild[3][i].text + ","
					bboxstring+=ggchild[3][3].text + ";"
			frameDict["frame_number"] = filename
			frameDict["RoIs"] = bboxstring
			frameList.append({"frame_number":filename, "RoIs": bboxstring})#, "Sign IDs": signIds, "Sign Classes": signClasses})

print(frameList)
data = {"output": {"frames":frameList}}
with open(output_file_name, 'w') as outfile:
    json.dump(data, outfile, sort_keys=True, indent=4 * '')

# data = '["output", {"frames":frameList}]'
