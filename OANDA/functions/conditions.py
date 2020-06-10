def check_ave_line(df):
    #　移動平均線
    num = [5,13,21]
    ave_line = []
    res = ""
    for j in range(3):
        sum = 0
        for i in range(num[j]):
            sum +=df['close'][-i-1]
        ave_line.append(sum/num[j])
    print(ave_line)

    if (ave_line[0]>ave_line[1]>ave_line[2]):
        res = "移動平均線が理想的に上昇"
    elif (ave_line[0]<ave_line[1]<ave_line[2]):
        res = "移動平均線が理想的に下降"
    return res