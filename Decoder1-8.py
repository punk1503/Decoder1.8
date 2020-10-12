from tkinter import *
from itertools import groupby
from textwrap import wrap
#перевод систем счисления
def convert_base(num, to_base=10, from_base=10):
    # first convert to decimal number
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    # now convert decimal to 'to_base' base
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]
#перевод ASCII 1251 символа в десятичный символ
def ascii_encode(character):

    if ord(character)>=32 and ord(character)<=126:
        return ord(character)
    elif ord(character)>=1040 and ord(character)<=1103:
        return ord(character)-848
    else:
        return '`'
#перевод десятичного кода в ASCII 1251 символ
def ascii_convert(ndx):

    key=list(range(32,127))
    key=key+list(range(192,256))

    value=[chr(i) for i in range(32, 127)]
    value=value+list([chr(i) for i in range(1040, 1104)])

    ascii_codes=dict(zip(key, value))
    if int(ndx) in ascii_codes:
        return ascii_codes[int(ndx)]
    else:
        return '`'
#функция нахождения XOR защитных бит для Хемминга
def xor(arr, xorStep):
	tmpArr = []
	for i in range(xorStep-1, len(arr), xorStep*2):
		for j in range(i, i+xorStep):
			tmpArr.append(arr[j])
	counter = tmpArr.count('1')
	if counter%2==1:
		return 1
	else: 
		return 0
#функция кодировки Элиаса
def alias_encode(alias):
    s=''
    for i in range(len(alias)):
        tmp=str(convert_base(ascii_encode(alias[i]), 2, 10))
        s+=(8-len(tmp))*'0'+tmp
    arr=[]
    first_num=s[0]
    arr=[''.join(g) for k, g in groupby(s)]
    first_num=s[0]
    final=''
    for i in range(len(arr)):
        arr[i]=str(convert_base(len(arr[i]), 2, 10))
        arr[i]=(len(arr[i])-1)*'0'+arr[i]
        final+=arr[i]
    final=first_num+final
    return final
#функция декодировки Элиаса
def alias_decode(alias):
    start=alias[0]
    alias=alias[1:]
    alias=alias.replace(' ', '')
    arr=[]
    while len(alias)>0:
        counter=0
        i=0
        while alias[i]!='1':
            counter+=1
            i+=1
        arr.append(alias[0:counter*2+1])
        alias=alias[counter*2+1:len(alias)]

    for i in range(len(arr)):
        arr[i]=convert_base(arr[i], 10, 2)

    for i in range(len(arr)):
        arr[i]=start*int(arr[i])
        if start=='1':
          start='0'
        else:
            start='1'
    s=''
    for i in range(len(arr)):
        s+=str(arr[i])
    s=wrap(s,8)
    return s
#функция кодировки хемминга
def hamming_encode(hamming):
    s=''
    for i in range(len(hamming)):
        tmp=str(convert_base(ascii_encode(hamming[i]), 2, 10))
        s+=(8-len(tmp))*'0'+tmp
    hamming=s
    final=''
    while len(hamming)>0:
        if len(hamming)<11:
            hamming+=(11-len(hamming))*'0'
        block=hamming[0:11]
        hamming=hamming[11:len(hamming)]
        arr_block=list(range(15))
        arr_block[0]=0
        arr_block[1]=0
        arr_block[3]=0
        arr_block[7]=0
        arr_block[2]=block[0]
        arr_block[4:7]=block[1:4]
        arr_block[8:15]=block[4:11]
        arr_block[0]=xor(arr_block, 1)
        arr_block[1]=xor(arr_block, 2)
        arr_block[3]=xor(arr_block, 4)
        arr_block[7]=xor(arr_block, 8)
        
        for i in range(len(arr_block)):
            final+=str(arr_block[i])
    return final
#функция декодировки Хемминга
def hamming_decode(hamming):
    hamming=hamming.replace(' ', '')
    final=''
    while(len(hamming) > 0):
        tmpArr = hamming[0:15]
        tmpArr = wrap(tmpArr, 1)
        hamming = hamming[15:len(hamming)]
        error = (xor(tmpArr, 8)*8 + xor(tmpArr, 4)*4 + xor(tmpArr, 2)*2 + xor(tmpArr, 1))-1
        if error<=0:
            error=0
        if tmpArr[error]=='1':
            tmpArr[error]='0'
        else:
            tmpArr[error]='1'
        del tmpArr[7]
        del tmpArr[3]
        del tmpArr[1]
        del tmpArr[0]
        for i in range(len(tmpArr)):
            final+=tmpArr[i]
    final = wrap(final, 8)
    return final
#обработка нажатия ЛКМ по кнопке 1
def button1_press(event):
    label4['text']='ASCII'
    func=modes.get()
    if func==1:
        arr=alias_decode(input_place.get())
    elif func==2:
        arr=hamming_decode(input_place.get())
    elif func==3:
        arr=input_place.get()
        arr=wrap(arr.replace(' ',''), 8)
        
    decimal_nums=''
    hex_nums=''
    ascii_chars=''
    for i in range(len(arr)):
        decimal_nums+=convert_base(arr[i], 10, 2)+' '
        hex_nums+=convert_base(arr[i], 16, 2)+' '
        ascii_chars+=ascii_convert(convert_base(arr[i], 10, 2))

    decimal_place.delete(0, END)
    hexadecimal_place.delete(0, END)
    ascii_place.delete(0, END)
    decimal_place.insert(0, decimal_nums)
    hexadecimal_place.insert(0, hex_nums)
    ascii_place.insert(0, ascii_chars)
#обработка нажатия ЛКМ по кнопке 2
def button2_press(event):
    input_place.delete(0, END)
    decimal_place.delete(0, END)
    hexadecimal_place.delete(0, END)
    ascii_place.delete(0, END)
#обработка нажатия ЛКМ по кнопке 3
def button3_press(event):
    label4['text']='Binary'
    func=modes.get()
    decimal_place.delete(0, END)
    hexadecimal_place.delete(0, END)
    ascii_place.delete(0, END)
    if func==1:
        decimal_place.insert(0, 'None')
        hexadecimal_place.insert(0, 'None')
        ascii_place.insert(0, alias_encode(input_place.get()))
    elif func==2:
        decimal_place.insert(0, 'None')
        hexadecimal_place.insert(0, 'None')
        ascii_place.insert(0, hamming_encode(input_place.get()))
    elif func==3:
        ascii_str=input_place.get()
        for i in range(len(ascii_str)):
            decimal_place.insert(END, str(ascii_encode(ascii_str[i]))+' ')
            hexadecimal_place.insert(END, str(convert_base(ascii_encode(ascii_str[i]), 16, 10))+' ')
            tmp_bin=str(convert_base(ascii_encode(ascii_str[i]), 2, 10))
            tmp_bin=(8-len(tmp_bin))*'0'+tmp_bin+' '
            ascii_place.insert(END, tmp_bin)


root = Tk()
root.title('Decoder')
root.geometry('430x220')
root.resizable(0,0)
root.iconbitmap('logo2.ico')

#надписи
label1=Label(root, text='Input:')
label2=Label(root, text='Decimal')
label3=Label(root, text='Hexadecimal')
label4=Label(root, text='ASCII')
label_version=Label(root, text='Decoder 1.8 beta', fg='gray', anchor='w')
label_guide1=Label(root, text='Decode принимает бинарную кодировку', fg='gray', anchor='w')
label_guide2=Label(root, text='Encode принимает ASCII символы, включая латиницу', fg='gray', anchor='w')
label_guide3=Label(root, text='Ctrl+C/Ctrl+V не работают при русской расскладке', fg='gray', anchor='w')

#блоки ввода и вывода
input_place = Entry(root)
decimal_place = Entry(root)
hexadecimal_place = Entry(root)
ascii_place = Entry(root)

#кнопки
button1 = Button(root, text='Decode')
button1.bind('<Button-1>', button1_press)
button2 = Button(root, text='Clear')
button2.bind('<Button-1>', button2_press)
button3 = Button(root, text='Encode')
button3.bind('<Button-1>', button3_press)

#блок radiobutton
modes = IntVar()
alias_radiobutton = Radiobutton(root, text='Alias', value=1, variable=modes, anchor='w')
hamming_radiobutton = Radiobutton(root, text='Hamming', value=2, variable=modes, anchor='w')
ascii_radiobutton = Radiobutton(root, text='ASCII(8 bit)', value=3, variable=modes, anchor='w')
modes.set(1)


label1.place(width=70, height=20, x=20, y=20)
label2.place(width=70, height=20, x=20, y=50)
label3.place(width=70, height=20, x=20, y=80)
label4.place(width=70, height=20, x=20, y=110)
label_version.place(x=1, y=200)
label_guide1.place(height=20, x=20, y=130)
label_guide2.place(height=20, x=20, y=150)
label_guide3.place(height=20, x=20, y=170)


input_place.place(width=210, height=20, x=100, y=20)
decimal_place.place(width=210, height=20, x=100, y=50)
hexadecimal_place.place(width=210, height=20, x=100, y=80)
ascii_place.place(width=210, height=20, x=100, y=110)

button1.place(width=60, height=20, x=320, y=20)
button2.place(width=60, height=20, x=320, y=80)
button3.place(width=60, height=20, x=320, y=50)

alias_radiobutton.place(width=90, height=20, x=320, y=110)
hamming_radiobutton.place(width=90, height=20, x=320, y=130)
ascii_radiobutton.place(width=90, height=20, x=320, y=150)
root.mainloop()