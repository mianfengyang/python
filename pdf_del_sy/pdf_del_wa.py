from PIL import Image
from itertools import product
import fitz

# 去除pdf的水印
def remove_pdfwatermark():
    #打开源pfd文件
    pdf_file = fitz.open("跟小鱼学习去水印.pdf")

    #page_no 设置为0
    page_no = 0
    #page在pdf文件中遍历
    for page in pdf_file:
        #获取每一页对应的图片pix (pix对象类似于我们上面看到的img对象，可以读取、修改它的 RGB)
        #page.get_pixmap() 这个操作是不可逆的，即能够实现从 PDF 到图片的转换，但修改图片 RGB 后无法应用到 PDF 上，只能输出为图片
        pix = page.get_pixmap()

        #遍历图片中的宽和高，如果像素的rgb值总和大于510，就认为是水印，转换成255，255,255-->即白色
        for pos in product(range(pix.width), range(pix.height)):
            if sum(pix.pixel(pos[0], pos[1])) >= 510:
                pix.set_pixel(pos[0], pos[1], (255, 255, 255))
        #保存去掉水印的截图
        pix.pil_save(f"./{page_no}.png", dpi=(30000, 30000))
        #打印结果
        print(f'第 {page_no} 页去除完成')

        page_no += 1

#去除的pdf水印添加到pdf文件中
def pictopdf():
	#水印截图所在的文件夹
    # pic_dir = input("请输入图片文件夹路径：")
	pic_dir = 'D:\Project\watemark'
	
	pdf = fitz.open()
	#图片数字文件先转换成int类型进行排序
	img_files = sorted(os.listdir(pic_dir), key=lambda x: int(str(x).split('.')[0]))
	for img in img_files:
	    print(img)
	    imgdoc = fitz.open(pic_dir + '/' + img)
	    #将打开后的图片转成单页pdf
	    pdfbytes = imgdoc.convertToPDF()
	    imgpdf = fitz.open("pdf", pdfbytes)
	    #将单页pdf插入到新的pdf文档中
	    pdf.insertPDF(imgpdf)
	pdf.save("跟小鱼学习去水印_完成.pdf")
	pdf.close()

if __name__ == '__main__':
    remove_pdfwatermark()
    pictopdf()