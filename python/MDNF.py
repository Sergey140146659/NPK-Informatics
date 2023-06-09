from browser import document, html, window, alert

def getbool(a):
    ans = ''
    c = 0
    for i in range(len(a)):
        if a[i] == '1':
            ans += chr(c + ord('a'))
            c += 1
        if a[i] == '0':
            ans += '!' + chr(c + ord('a'))
            c += 1
    return ans
 
 
def get_alone(s, f):
    ans = 1
    for i in range(len(s)):
        if s[0] == '!' and i == 0:
            continue
        if s[i] == '!':
            continue
        if s[i - 1] == '!':
            ans *= ((f[s[i]] + 1) % 2)
        else:
            ans *= f[s[i]]
    return ans
 
 
def get_func(s, f):
    ans = 0
    for i in s:
        ans |= get_alone(i, f)
    return ans
 
 
def check(s1, s2, cnt):
    s3 = ''
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            s3 += '*'
            if s1[i] == '*' or s2[i] == '*':
                return -1
        else:
            s3 += s1[i]
    if s3.count('*') != cnt:
        return -1
    return s3
 
 
def iteration(a, cnt):
    next_a = set()
    minterms = set()
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            x = check(a[i], a[j], cnt)
            if x != -1:
                minterms.add('(' + a[i] + ', ' + a[j] + ') = ' + x)
                next_a.add(x)
 
    return [sorted(list(next_a)), sorted(list(minterms))]
 
 
def to_letters(a):
    s = ''
    for i in range(len(a)):
        if (a[i] == '*'):
            s += '*'
            continue
        if a[i] == '1':
            s += chr(i + ord('a'))
        else:
            s += '!'
            s += chr(i + ord('a'))
    return s
 
 
def a_letters(a):
    ans = []
    mx = 0
    for i in a:
        ans.append(to_letters(i))
        mx = max(mx, len(to_letters(i)))
    for i in range(len(ans)):
        while len(ans[i]) < mx:
            ans[i] += ' '
    return ans
 
 
def main(s, n):
    a = s.split(" + ")
    a_new = []
    for i in a:
        s = ''
        last = 0
        for j in range(len(i)):
            if i[j] == '!':
                s += '0'
                last = 1
            else:
                if last == 0:
                    s += '1'
                else:
                    last = 0
        a_new.append(s)
    a = a_new
    max_len = len(a)
    last_a = a
    cnt = 1
    total_a = []
    total_terms = []
    total_a_letters = []
 
    while len(a) != 0:
        total_a.append(a)
        total_a_letters.append(a_letters(a))
        last_a = a
        a_x = iteration(a, cnt)
        total_terms.append(a_x[1])
        a = a_x[0]
        cnt += 1
        max_len = max(max_len, len(a))
        max_len = max(max_len, len(a_x[1]))
    len_last = len(last_a)
    for i in range(len(total_a)):
        while len(total_a_letters[i]) < max_len:
            total_a_letters[i].append(' ' * len(total_a_letters[i][-1]))
        while len(total_a[i]) < max_len:
            total_a[i].append(' ' * len(total_a[i][-1]))
        while len(total_terms[i]) < max_len:
            if i == len(total_a) - 1:
                break
            total_terms[i].append(' ' * len(total_terms[i][-1]))
    total_ans = ''
    for i in range(len(total_a) - 1):
        total_ans += str(i + 1) + '-й шаг алгоритма\n'
        for j in range(len(total_a[i])):
            total_ans += total_a_letters[i][j] + ' ' * 5 + total_a[i][j] + ' ' * 5 + total_terms[i][j] + ' ' * 5 + \
                         total_a[i + 1][j] + '\n'
        total_ans += '\n'
    ans = ''
    last_a = a_letters(last_a[0:len_last])
    for pos in range(len(last_a)):
        cur_ans = ''
        for j in range(len(last_a[pos])):
            if last_a[pos][j] != '*':
                cur_ans += last_a[pos][j]
        ans += cur_ans
        ans += ' + '
    ans = ans[0:len(a) - 2]
    total_ans += "Дальнейшее комбинирование невозможно, итог:\n"
 
    terms = sorted(ans.split(" + "))
    for i in range(len(terms)):
        while terms[i][-1] == ' ':
            terms[i] = terms[i][0:len(terms[i]) - 1]
    all_equal = []
    all_deleted = []
    all_var = ''
    for i in range(ord('a'), ord('a') + n):
        all_var += chr(i)
    for mask_delete in range(1, (1 << (len(terms) + 1))):
        cur_term = []
        cur_deleted = []
        for bit in range(len(terms)):
            if (mask_delete >> bit) & 1:
                cur_term.append(terms[bit])
            else:
                cur_deleted.append(terms[bit])
        equal = 1
        for mask_bool in range((1 << (n + 1))):
            f = {}
            for bit in range(n):
                f[all_var[bit]] = ((mask_bool >> bit) & 1)
            equal &= (get_func(terms, f) == get_func(cur_term, f))
        if equal:
            all_equal.append(sorted(cur_term))
            all_deleted.append(sorted(cur_deleted))
    min_cnt = len(terms)
    our_min_dnf = terms
    deleted = []
    for i in range(len(all_equal)):
        if len(all_equal[i]) < min_cnt:
            min_cnt = len(all_equal[i])
            our_min_dnf = all_equal[i]
            deleted = all_deleted[i]
    for i in last_a:
        total_ans += i + '\n'
    if min_cnt != len(terms):
        total_ans += "\nФункция f = " + ans + " является избыточной\n"
        total_ans += "Исключаем: " + ', '.join(deleted)
        total_ans += "\nf = " + ' + '.join(our_min_dnf)
 
    else:
        total_ans += "\nf = " + ans
    total_ans += "\n"*2
    return total_ans


def senddata(event):
    num = int(document["num_input"].value)
    str = document["str_input"].value
    taera = document["textar"]
    taera.value = main(str, num)
   
document["sendbutton"].bind("click", senddata)