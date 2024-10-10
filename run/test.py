import numpy as np
import re

def generate_interpolated_lines_formatted(start_str, end_str, n):
    """
    生成在起始和末尾数据行之间的n条均匀插值数据行，保持数字的长度和空格间距一致。
    
    参数:
    - start_str (str): 起始数据行，空格分隔的数值字符串。
    - end_str (str): 末尾数据行，空格分隔的数值字符串。
    - n (int): 要插入的中间数据行数。
    
    返回:
    - list of str: 包含n条插值数据行的列表，每条数据行是空格分隔的数值字符串。
    """
    # 使用正则表达式分割字符串，保留分隔符（空格）
    def split_with_spaces(s):
        return re.findall(r'\s+|\S+', s)
    
    start_parts = split_with_spaces(start_str)
    end_parts = split_with_spaces(end_str)
    
    # 提取数字部分的索引
    num_indices = [i for i, part in enumerate(start_parts) if not part.isspace()]
    
    # 调试信息
    print("=== Debug Information ===")
    print(f"Start Parts: {start_parts}")
    print(f"End Parts: {end_parts}")
    print(f"Number Indices: {num_indices}")
    
    # 提取数字字符串
    start_nums_str = [start_parts[i] for i in num_indices]
    end_nums_str = [end_parts[i] for i in num_indices]
    
    # 更多调试信息
    print(f"Start Numbers: {start_nums_str}")
    print(f"End Numbers: {end_nums_str}")
    
    if len(start_nums_str) != len(end_nums_str):
        raise ValueError("起始和末尾数据行的数值数量必须相同。")
    
    num_columns = len(start_nums_str)
    
    # 确定每列的格式
    formats = []
    for col in range(num_columns):
        start_num = start_nums_str[col]
        end_num = end_nums_str[col]
        
        # 确定小数位数
        def count_decimal(s):
            if '.' in s:
                return len(s.split('.')[-1])
            else:
                return 0
        
        decimals_start = count_decimal(start_num)
        decimals_end = count_decimal(end_num)
        decimals = max(decimals_start, decimals_end)
        
        # 确定宽度（包括负号和小数点）
        width_start = len(start_num)
        width_end = len(end_num)
        width = max(width_start, width_end)
        
        # 创建格式字符串，例如 '{:6.2f}'
        fmt = f"{{:>{width}.{decimals}f}}"
        formats.append(fmt)
    
    # 将数字字符串转换为浮点数
    start_vals = list(map(float, start_nums_str))
    end_vals = list(map(float, end_nums_str))
    
    # 转换为NumPy数组
    start_array = np.array(start_vals)
    end_array = np.array(end_vals)
    
    # 生成插值系数
    interpolated_lines = []
    for i in range(1, n + 1):
        factor = i / (n + 1)
        interp_array = start_array + factor * (end_array - start_array)
        
        # 格式化每个数字
        formatted_nums = [formats[col].format(interp_array[col]) for col in range(num_columns)]
        
        # 重建行，保留原有的空格分隔
        new_parts = start_parts.copy()
        for idx, col in enumerate(num_indices):
            new_parts[col] = formatted_nums[idx]
        
        # 合并所有部分
        interp_str = ''.join(new_parts)
        interpolated_lines.append(interp_str)
    
    return interpolated_lines
if __name__ == "__main__":
    # 示例 1
    start_line = "0.00  0.0 0.0\n"
    end_line = "1.0 1.0 1.0"
    n = 3
    interpolated = generate_interpolated_lines_formatted(start_line, end_line, n)
    print("示例 1:")
    for idx, line in enumerate(interpolated, 1):
        print(f"中间数据行 {idx}: '{line}'")
    
    print("\n")
    
    # 示例 2
    start_line = "10  20  30  40"
    end_line = "50  60  70  80"
    n = 4
    interpolated = generate_interpolated_lines_formatted(start_line, end_line, n)
    print("示例 2:")
    for idx, line in enumerate(interpolated, 1):
        print(f"中间数据行 {idx}: '{line}'")
    
    print("\n")
    
    # 示例 3：两列数据
    start_line = "4992 25"
    end_line = "5000 30"
    n = 3
    interpolated = generate_interpolated_lines_formatted(start_line, end_line, n)
    print("示例 3:")
    for idx, line in enumerate(interpolated, 1):
        print(f"中间数据行 {idx}: '{line}'")
