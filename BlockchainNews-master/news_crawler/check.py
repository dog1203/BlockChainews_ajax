


def check_future(line):
    # words = ['区块链', '比特币', '区块', 'blockchain', '山寨币', '空气币', '币币交易']
    words = ['将', '预计', '明天', '后天', '下周', '月底', '明日', '明晚', '下月', '明年', '未来', '计划于', '准备于']
    for word in words:
        if line.find(word) != -1:
            return True
    return False


def check_blacklist(line):
    blacklist = ['未来网', '未来医疗']
    if line in blacklist:
        return False
    return True