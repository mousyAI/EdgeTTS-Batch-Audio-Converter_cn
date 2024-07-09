import os
### print当前文件位置
current_path = os.getcwd()
print(current_path)

### 设置speaker的音色/语种
import json

config_path = os.path.join(current_path, 'config.json')
with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)
    # 获取所有的speakers值
    chosen_speakers = config_data.get('speakers', [])
    for speaker in chosen_speakers:
        print(speaker)

import glob
# 假设current_path已经定义并获取到了当前工作目录
txt_folder = os.path.join(current_path, 'txts')
output_folder = os.path.join(current_path, 'outputs')
# 检查txts文件夹是否存在，如果不存在则创建
if not os.path.exists(txt_folder):
    os.makedirs(txt_folder)
    print("The 'txts' folder was not found, so it has been created. Please place your .txt files in the 'txts' folder.")

# 使用glob.glob查找txts文件夹下的所有.txt文件
txt_files = glob.glob(os.path.join(txt_folder, '*.txt'))

# 如果txt_files为空，说明txts文件夹内目前没有.txt文件，给出提示
if not txt_files:
    print("No .txt files were found in the 'txts' folder. Please add your .txt files and try again.")
else:
    print("Found .txt files:")
    for file in txt_files:
        print(file)

    # 如果需要读取文件内容到列表的代码保持不变
    texts = []
    filenames_only =[]
    for file_path in txt_files:
        text = None
        encodings = ['utf-8', 'GBK', None]
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    text = file.read()
                    break
            except UnicodeDecodeError:
                continue
            except TypeError:
                pass

        if text is None:
            print(f"Failed to read {file_path} with any of the attempted encodings.")
            continue

        texts.append(text)
        filename = os.path.splitext(os.path.basename(file_path))[0]
        filenames_only.append(filename)

print(txt_files)

import edge_tts

for chosen_speaker in chosen_speakers:
    for text in texts:
        MAX_RETRIES = 5  # 最大重试次数
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                # 尝试执行的代码块
                text_idx = texts.index(text)
                OUTPUT_FILE =  os.path.join(output_folder, filenames_only[text_idx]+ '_' + chosen_speaker +".mp3" )
                communicate = edge_tts.Communicate(text, chosen_speaker)
                communicate.save_sync(OUTPUT_FILE)
                print("操作" + filenames_only[text_idx] + "成功，speaker是:", chosen_speaker)
                break  # 如果没有异常，跳出循环
            except Exception as e:
                print(f"第{retry_count + 1}次尝试失败，原因是: {e}")
                retry_count += 1
                if retry_count < MAX_RETRIES:
                    print("准备重新尝试...")
                else:
                    print("已达到最大重试次数，不再尝试。")
