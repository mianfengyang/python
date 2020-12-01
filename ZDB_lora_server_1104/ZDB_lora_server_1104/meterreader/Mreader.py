import os
import cv2
import sys
import numpy as np
import math

def gray_histcheck(in_IMG,base_IMG):
	in_GRAY=cv2.imread(in_IMG,0)
	base_GRAY=cv2.imread(base_IMG,0)
	in_HIST=cv2.calcHist([in_GRAY],[0],None,[256],[0,256])
	base_HIST=cv2.calcHist([base_GRAY],[0],None,[256],[0,256])
	miu_in=in_HIST.sum()/256
	miu_base=base_HIST.sum()/256
	delta2_in=0
	delta2_base=0
	for i in range(256):
		delta2_in+=(in_HIST[i]-miu_in)**2	
		delta2_base+=(base_HIST[i]-miu_base)**2	
	delta2_in/=in_HIST.sum()
	delta2_base/=base_HIST.sum()
	if abs(delta2_base-delta2_in)>1500:
		flag=5#ERROR TYPE 5
	else:
		flag=0
	return flag

def gray_smaller(in_GRAY,in_c_x,in_c_y,in_range,in_m,in_n):
	if in_c_x<=in_range:
		out_n=in_range+in_c_x
	elif in_c_x+in_range>=in_n:
		out_n=in_range-in_c_x+in_n
	else:
		out_n=2*in_range
	if in_c_y<=in_range:
		out_m=in_range+in_c_y
	elif in_c_y+in_range>=in_m:
		out_m=in_range-in_c_y+in_m
	else:
		out_m=2*in_range
	out_x=max(0,in_c_x-in_range)
	out_y=max(0,in_c_y-in_range)
	out_GRAY=np.zeros((out_m,out_n),dtype=np.uint8)
	for i in range(out_m):
		for j in range(out_n):
			out_GRAY[i][j]=in_GRAY[min(out_y+i,in_m)][min(out_x+j,in_n)]
	return out_GRAY,out_x,out_y,out_m,out_n

def gray_bigger(in_GRAY,in_x,in_y,in_m,in_n,out_m,out_n):
	out_GRAY=np.zeros((out_m,out_n),dtype=np.uint8)
	for i in range(out_m):
		for j in range(out_n):
			if i>=in_y and i<in_y+in_m and j>=in_x and j<in_x+in_n:
				out_GRAY[i][j]=in_GRAY[i-in_y][j-in_x]
			else:
				out_GRAY[i][j]=0
	return out_GRAY

def bw_bigger(in_BW,in_x,in_y,in_m,in_n,out_m,out_n):
	out_BW=np.zeros((out_m,out_n),dtype=np.uint8)
	for i in range(out_m):
		for j in range(out_n):
			if i>=in_y and i<in_y+in_m and j>=in_x and j<in_x+in_n:
				out_BW[i][j]=in_BW[i-in_y][j-in_x]
			else:
				out_BW[i][j]=0
	return out_BW

def bw_skeletonization(in_BW):
	ELE=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))###20200310
	out_BW=np.zeros(in_BW.shape,np.uint8)
	TEMP=np.zeros(in_BW.shape,np.uint8)
	i=0
	while True:
		TEMP=cv2.morphologyEx(in_BW,cv2.MORPH_OPEN,ELE)
		TEMP=cv2.bitwise_not(TEMP)
		TEMP=cv2.bitwise_and(in_BW,TEMP)
		out_BW=cv2.bitwise_or(out_BW,TEMP)
		in_BW=cv2.erode(in_BW,ELE)
		min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(in_BW)
		if max_val==.0:
			break
	return out_BW

def bw_hough(in_BW,x1,y1):###20200401
	in_m,in_n=in_BW.shape[0:2]
	width_hough=int(0.7*(320+240)+240+1.5)
	HOUGH=np.zeros((181,width_hough),dtype=np.uint16)
	hm=0
	for i in range(in_m):
		for j in range(in_n):
			if in_BW[i][j]==255:
				for k in range(181):
					temp=int(i*np.cos(k)+j*np.sin(k)+in_m)
					HOUGH[k][temp]+=1
	hm=HOUGH.max()
	theta_m=HOUGH.argmax()//width_hough
	rho_m=HOUGH.argmax()%width_hough
	_acc=0
	_max=0
	_min=10000
	pointer_points=[]#
	for i in range(in_m):
		for j in range(in_n):
			if in_BW[i][j]==255:
				temp=int(i*np.cos(theta_m)+j*np.sin(theta_m)+in_m)
				if temp==rho_m:
					pointer_points.append([i,j])#
					s_temp=(i-y1)**2+(j-x1)**2
					if s_temp<_min:
						_min=s_temp
						yo=i
						xo=j
	points_num=len(pointer_points)
	counter1=0
	for i in pointer_points:
		if i==[yo,xo]:
			break
		counter1+=1
	counter2=points_num-counter1-1
	if counter1>=counter2:
		yp,xp=pointer_points[0]
	else:
		yp,xp=pointer_points[points_num-1]
	if abs(counter1-counter2)/min(counter1,counter2)<=0.1:
		breakmax=0
		for i in range(points_num-1):#
			breaktemp=(pointer_points[i][0]-pointer_points[i+1][0])**2+(pointer_points[i][1]-pointer_points[i+1][1])**2	
			if breaktemp>breakmax:
				breakmax=breaktemp
				break_y=pointer_points[i][0]
				break_x=pointer_points[i][1]
		yp1,xp1=pointer_points[0]
		d1=(yp1-break_y)**2+(xp1-break_x)**2
		yp2,xp2=pointer_points[points_num-1]
		d2=(yp2-break_y)**2+(xp2-break_x)**2
		if d1>d2:
			yp=yp1
			xp=xp1
		else:
			yp=yp2
			xp=xp2
	return xo,yo,xp,yp

def angle_calculation(x,y,x_l,y_l,x_r,y_r):
	denominator=((x_l-x)**2+(y_l-y)**2)**0.5*((x_r-x)**2+(y_r-y)**2)**0.5
	if denominator==0:
		angle=0
	else:
		angle=np.arccos(((x_l-x)*(x_r-x)+(y_l-y)*(y_r-y))/denominator)
	return angle

def cross_calculation(x1,y1,x2,y2,x3,y3,x4,y4):
	denominator=x4*y2+x3*y1+x2*y3+x1*y4-x4*y1-x3*y2-x2*y4-x1*y3
	if denominator==0:
		x=float('inf')
		y=float('inf')
	else:
		x=(y4*x3*x1+y3*x4*x2+y2*x1*x4+y1*x2*x3-y4*x3*x2-y3*x4*x1-y2*x1*x3-y1*x2*x4)/denominator
		y=(y4*x3*y1+y3*x4*y2+y2*x1*y4+y1*x2*y3-y4*x3*y2-y3*x4*y1-y2*x1*y3-y1*x2*y4)/denominator
	return x,y

def meter_info(max_value,first_value,x,y,xb_,yb_,xe_,ye_,xf_,yf_):
	L=angle_calculation(x,y,xb_,yb_,xf_,yf_)
	L=L*180/np.pi
	M=angle_calculation(x,y,xb_,yb_,xe_,ye_)
	M=M*180/np.pi
	R=360-L-M
	factor=(max_value-first_value)/R
	return L,M,R,factor

def meter_calculation(L,M,R,_factor,_first,_max,xo,yo,xp,yp,x,y,xb_,yb_,xe_,ye_,xf_,yf_):
	flag=0
	P_TO_begin=angle_calculation(x,y,xp,yp,xb_,yb_)
	P_TO_begin=P_TO_begin*180/np.pi
	P_TO_first=angle_calculation(x,y,xp,yp,xf_,yf_)
	P_TO_first=P_TO_first*180/np.pi
	P_TO_end=angle_calculation(x,y,xp,yp,xe_,ye_)
	P_TO_end=P_TO_end*180/np.pi
	if (P_TO_begin+P_TO_first<=L+5)or(P_TO_begin<5 and P_TO_first<=L+5):#in L
	#	print("A")
		if P_TO_begin<=L/5:
			result=0
		else:
			result=_first-_factor*P_TO_first
	elif P_TO_begin>=P_TO_first:#in R
	#	print("B")
		result=_first+_factor*P_TO_first
	elif P_TO_begin<P_TO_first:#in R
	#	print("C")
		result=_first+_factor*(360-L-P_TO_begin)	
	else:#in M  
		result=0
		flag=7#ERROR TYPE 7
	if result>_max:
		result=0
		flag=8#ERROR TYPE 8
	#print("result",result)
	return flag,result

def meter_reader_base(meter_name,base_img,base_txt):
	flag=0
	version=r'20200120'
	###READ
	try:
		file=open(base_txt)
	except IOError:
		flag=1#ERROR TYPE 1
		return flag,version
	try:
		img=cv2.imread(base_img,0)
	except IOError:
		flag=2#ERROR TYPE 2
		return flag,version
	data=file.readlines()
	data=[x.strip() for x in data if x.strip()!='']
	point_1=data[0]+'\n'
	p1=point_1.split(',')
	x1=int(p1[0])
	y1=int(p1[1])
	point_2=data[1]+'\n'
	p2=point_2.split(',')
	x2=int(p2[0])
	y2=int(p2[1])
	point_3=data[2]+'\n'
	p3=point_3.split(',')
	x3=int(p3[0])
	y3=int(p3[1])
	point_4=data[3]+'\n'
	p4=point_4.split(',')
	x4=int(p4[0])
	y4=int(p4[1])
	point_5=data[4]+'\n'
	p5=point_5.split(',')
	x5=int(p5[0])
	y5=int(p5[1])
	point_6=data[5]+'\n'
	p6=point_6.split(',')
	x6=int(p6[0])
	y6=int(p6[1])
	outer_max_value=float(data[6])
	inner_max_value=float(data[7])
	outer_first_value=float(data[8])
	inner_first_value=float(data[9])	
	outer_unit=data[10]
	inner_unit=data[11]
	L_outer,M_outer,R_outer,factor_outer=meter_info(outer_max_value,outer_first_value,x1,y1,x2,y2,x3,y3,x5,y5)
	L_inner,M_inner,R_inner,factor_inner=meter_info(inner_max_value,inner_first_value,x1,y1,x2,y2,x4,y4,x6,y6)
	R2=(x2-x1)**2+(y2-y1)**2
	###WRITE
	save_path=r'/data/pyfuc/'
	#save_path='./'#
	isExist=os.path.exists(save_path)
	if not isExist:
		os.makedirs(save_path)
	full_path_img=save_path+'base_'+str(meter_name)+'.jpg'
	cv2.imwrite(full_path_img,img)	
	full_path_txt=save_path+'base_'+str(meter_name)+'.txt'
	file=open(full_path_txt,'w')
	file.write(point_1)
	file.write(point_2)
	file.write(point_3)
	file.write(point_4)
	file.write(point_5)
	file.write(point_6)
	file.write(str(outer_max_value)+'\n')
	file.write(str(inner_max_value)+'\n')
	file.write(str(outer_first_value)+'\n')
	file.write(str(inner_first_value)+'\n')
	file.write(outer_unit+'\n')
	file.write(inner_unit+'\n')
	file.write(str(L_outer)+'\n')
	file.write(str(M_outer)+'\n')
	file.write(str(R_outer)+'\n')
	file.write(str(factor_outer)+'\n')
	file.write(str(L_inner)+'\n')
	file.write(str(M_inner)+'\n')
	file.write(str(R_inner)+'\n')
	file.write(str(factor_inner)+'\n')
	file.write(str(R2)+'\n')
	return flag,version
	
def meter_reader_now(full_path_txt, full_path_jpg, now_img):
	flag=0
	version=r'20200120'
	###READ
	#save_path=r'/data/pyfuc/'
	#isExist=os.path.exists(save_path)
	#if not isExist:
	#	os.makedirs(save_path)
	#full_path_txt=save_path+'base_'+str(meter_name)+'.txt'
	#full_path_jpg=save_path+'base_'+str(meter_name)+'.jpg'
	if not os.path.exists(full_path_txt):
		print('Error: file {} does not exist! '.format(full_path_txt))
		flag=3#ERROR TYPE 3
		return flag,0,0,0
	if not os.path.exists(full_path_jpg):
		print('Error: file {} does not exist! '.format(full_path_jpg))
		flag=3#ERROR TYPE 3
		return flag,0,0,0
	try:
		file=open(full_path_txt)
	except IOError:
		flag=3#ERROR TYPE 3
		return flag,0,0,0
	try:
		IMG=cv2.imread(now_img)
	except IOError:
		flag=4#ERROR TYPE 4
		return flag,0,0,0
	GRAY=cv2.imread(now_img,0)
	flag=gray_histcheck(now_img,full_path_jpg)#ERROR TYPE 5
	if flag==5:
		return flag,0,0,0
	data=file.readlines()
	data=[x.strip() for x in data if x.strip()!='']
	point1=data[0]
	p1=point1.split(',')
	x1=int(p1[0])
	y1=int(p1[1])
	point2=data[1]
	p2=point2.split(',')
	x2=int(p2[0])
	y2=int(p2[1])
	point3=data[2]
	p3=point3.split(',')
	x3=int(p3[0])
	y3=int(p3[1])
	point4=data[3]
	p4=point4.split(',')
	x4=int(p4[0])
	y4=int(p4[1])
	point5=data[4]
	p5=point5.split(',')
	x5=int(p5[0])
	y5=int(p5[1])
	point6=data[5]
	p6=point6.split(',')
	x6=int(p6[0])
	y6=int(p6[1])
	outer_max=float(data[6])
	inner_max=float(data[7])
	outer_first=float(data[8])
	inner_first=float(data[9])
	outer_unit=data[10]
	inner_unit=data[11]
	L_outer=float(data[12])
	M_outer=float(data[13])
	R_outer=float(data[14])
	factor_outer=float(data[15])
	L_inner=float(data[16])
	M_inner=float(data[17])
	R_inner=float(data[18])
	factor_inner=float(data[19])
	R2=float(data[20])
	
	###AVE
	GRAY=cv2.blur(GRAY,(3,3))
	GRAY=cv2.blur(GRAY,(3,3))
	
	###SMALLER
	m,n=GRAY.shape[0:2]
	r=int(R2**0.5)
	rrange=int(1.2*r)
	SMALL_GRAY,SMALL_x,SMALL_y,SMALL_m,SMALL_n=gray_smaller(GRAY,x1,y1,rrange,m,n)
	#cv2.imshow("SMALL_GRAY",SMALL_GRAY)###	
	#cv2.waitKey(0)###
	
	###GRAY2BW
	xxx,SMALL_BW=cv2.threshold(SMALL_GRAY,0,255,cv2.THRESH_OTSU)
	#cv2.imshow("SMALL_BW",SMALL_BW)###	
	#cv2.waitKey(0)###
	
	###NOT
	SMALL_BW=cv2.bitwise_not(SMALL_BW)
	
	###BIGGER
	BW=bw_bigger(SMALL_BW,SMALL_x,SMALL_y,SMALL_m,SMALL_n,m,n)	
	#cv2.imshow("BW",BW)###	
	#cv2.waitKey(0)###
	
	###DELETE
	m,n=BW.shape[0:2]
	for i in range(m):
		for j in range(n):
			L2=(j-x1)**2+(i-y1)**2
			if L2>R2:
				BW[i][j]=0
	#cv2.imshow("DELETE_BW",BW)###	
	#cv2.waitKey(0)###

	###SKEL
	SKEL=bw_skeletonization(BW)
	#cv2.imshow("SKEL",SKEL)###	
	#cv2.waitKey(0)###
	
	###DILATE
	kernal=np.ones((3,3),np.uint8)
	SKEL=cv2.dilate(SKEL,kernal)
	#cv2.imshow("DILATE",SKEL)###	
	#cv2.waitKey(0)###
	###HOUGH
	xo,yo,xp,yp=bw_hough(SKEL,x1,y1)

	flag,result_outer= meter_calculation(L_outer,M_outer,R_outer,factor_outer,outer_first,outer_max,xo,yo,xp,yp,x1,y1,x2,y2,x3,y3,x5,y5)#ERROR TYPE 7 8
	flag,result_inner= meter_calculation(L_inner,M_inner,R_inner,factor_inner,inner_first,inner_max,xo,yo,xp,yp,x1,y1,x2,y2,x4,y4,x6,y6)#ERROR TYPE 7 8

	###WRITE
	cv2.line(IMG,(xo,yo),(xp,yp),(201,145,142),2)
	cv2.circle(IMG,(xp,yp),2,(255,0,128),2)
	cv2.circle(IMG,(x1,y1),2,(0,255,255),2)
	#cv2.imshow("IMG",IMG)###
	#cv2.waitKey(0)###
	result_outer=round(result_outer,2)
	result_inner=round(result_inner,2)
	cv2.putText(IMG,str(result_outer),(10,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
	cv2.putText(IMG,outer_unit,(110,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
	cv2.putText(IMG,str(result_inner),(10,55),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
	cv2.putText(IMG,inner_unit,(110,55),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
	#cv2.putText(IMG,str(now_img),(0,200),cv2.FONT_HERSHEY_COMPLEX,0.3,(0,0,255),1)#
	return flag,result_outer,result_inner,IMG

def meter_adjustment_HOUGHCIRCLE(meter_name,img_now):
	flag=0
	###READ
	save_path=r'/data/pyfuc/'
	isExist=os.path.exists(save_path)
	if not isExist:
		os.makedirs(save_path)
	version=r'20200120'
	root_path='/'
	save_path=root_path+version+'/'
	full_path_img=save_path+'base_'+str(meter_name)+'.jpg'
	full_path_txt=save_path+'base_'+str(meter_name)+'.txt'
	try:
		file=open(full_path_txt)
	except IOError:
		flag=9#ERROR TYPE 9
		return flag,0
	try:
		IMG_B=cv2.imread(full_path_img)
	except IOError:
		flag=10#ERROR TYPE 10
		return flag,0
	try:
		IMG_N=cv2.imread(img_now)
	except IOError:
		flag=11#ERROR TYPE 11
		return flag,0
	GRAY_B=cv2.imread(full_path_img,0)
	GRAY_N=cv2.imread(img_now,0)
	data=file.readlines()
	data=[x.strip() for x in data if x.strip()!='']
	point1=data[0]
	p1=point1.split(',')
	x1=int(p1[0])
	y1=int(p1[1])
	point2=data[1]
	p2=point2.split(',')
	x2=int(p2[0])
	y2=int(p2[1])
	point3=data[2]
	p3=point3.split(',')
	x3=int(p3[0])
	y3=int(p3[1])
	point4=data[3]
	p4=point4.split(',')
	x4=int(p4[0])
	y4=int(p4[1])
	point5=data[4]
	p5=point5.split(',')
	x5=int(p5[0])
	y5=int(p5[1])
	point6=data[5]
	p6=point6.split(',')
	x6=int(p6[0])
	y6=int(p6[1])
	outer_max=float(data[6])
	inner_max=float(data[7])
	outer_first=float(data[8])
	inner_first=float(data[9])
	outer_unit=data[10]
	inner_unit=data[11]
	L_outer=float(data[12])
	M_outer=float(data[13])
	R_outer=float(data[14])
	factor_outer=float(data[15])
	L_inner=float(data[16])
	M_inner=float(data[17])
	R_inner=float(data[18])
	factor_inner=float(data[19])
	R2=float(data[20])
	
	###REWRITE IMG
	full_path_img=save_path+'base_'+str(meter_name)+'.jpg'
	cv2.imwrite(full_path_img,IMG_N)	
	
	#####SOBEL
	GRAY_N=cv2.equalizeHist(GRAY_N)
	x_g=cv2.Sobel(GRAY_N,-1,1,0,ksize=1)
	y_g=cv2.Sobel(GRAY_N,-1,0,1,ksize=1)
	absx=cv2.convertScaleAbs(x_g)
	absy=cv2.convertScaleAbs(y_g)
	GRAY_N=cv2.addWeighted(absx,0.5,absy,0.5,0)
	#xxx,dist=cv2.threshold(dist,0,255,cv2.THRESH_OTSU)
	#kernal=np.ones((3,3),np.uint8)
	#dist=cv2.dilate(dist,kernal)
	#cv2.imshow("SOBEL",GRAY_N)#
	#cv2.waitKey(0)#

	###HOUGH CIRCLE
	CIRCLE_B=cv2.HoughCircles(GRAY_B,
							  method=cv2.HOUGH_GRADIENT,
							  dp=1,
							  minDist=50,
							  circles=None,
							  param1=100,
							  param2=30,
							  minRadius=int(R2**0.5-10),
							  maxRadius=int(R2**0.5+30))
	CIRCLE_N=cv2.HoughCircles(GRAY_N,
							  method=cv2.HOUGH_GRADIENT,
							  dp=1,
							  minDist=50,
							  circles=None,
							  param1=100,
							  param2=30,
							  minRadius=int(R2**0.5-10),
							  maxRadius=int(R2**0.5+30))
	try:
		circles_b=CIRCLE_B[0,:,:]
	except TypeError:
		flag=12#ERROR TYPE 12
	else:
		try:
			circles_n=CIRCLE_N[0,:,:]
		except TypeError:
			flag=13#ERROR TYPE 13
		else:
			for i_b in circles_b[:]:
				for i_n in circles_n[:]:	
					x1_new=int(i_n[0])
					y1_new=int(i_n[1])
					if (x1_new-x1)**2+(y1_new-y1)**2<=450:
						cv2.circle(IMG_N,(i_n[0],i_n[1]),i_n[2],(0,128,255),2)#
						cv2.circle(IMG_N,(i_n[0],i_n[1]),2,(255,255,0),2)#
						point1=str(x1_new)+','+str(y1_new)
						x2_new=int(x2+i_n[0]-x1)
						y2_new=int(y2+i_n[1]-y1)
						point2=str(x2_new)+','+str(y2_new)
						x3_new=int(x3+i_n[0]-x1)
						y3_new=int(y3+i_n[1]-y1)
						point3=str(x3_new)+','+str(y3_new)
						x4_new=int(x4+i_n[0]-x1)
						y4_new=int(y4+i_n[1]-y1)
						point4=str(x4_new)+','+str(y4_new)
						x5_new=int(x5+i_n[0]-x1)
						y5_new=int(y5+i_n[1]-y1)
						point5=str(x5_new)+','+str(y5_new)
						x6_new=int(x6+i_n[0]-x1)
						y6_new=int(y6+i_n[1]-y1)
						cv2.circle(IMG_N,(x1,y1),2,(255,128,255),2)#
						cv2.circle(IMG_N,(x1_new,y1_new),2,(0,255,255),2)#
					else:
						flag=14#ERROR TYPE 14

	###REWRITE TXT
	full_path_txt=save_path+'base_'+str(meter_name)+'.txt'
	file=open(full_path_txt,'w')
	file.write(point1+'\n')
	file.write(point2+'\n')
	file.write(point3+'\n')
	file.write(point4+'\n')
	file.write(point5+'\n')
	file.write(point6+'\n')
	file.write(str(outer_max)+'\n')
	file.write(str(inner_max)+'\n')
	file.write(str(outer_first)+'\n')
	file.write(str(inner_first)+'\n')
	file.write(outer_unit+'\n')
	file.write(inner_unit+'\n')
	file.write(str(L_outer)+'\n')
	file.write(str(M_outer)+'\n')
	file.write(str(R_outer)+'\n')
	file.write(str(factor_outer)+'\n')
	file.write(str(L_inner)+'\n')
	file.write(str(M_inner)+'\n')
	file.write(str(R_inner)+'\n')
	file.write(str(factor_inner)+'\n')
	file.write(str(R2)+'\n')
	return flag,IMG_N
'''
def meter_adjustment_ORB(meter_name,img_before,img_now):
	IMG_B=cv2.imread(img_before)
	IMG_N=cv2.imread(img_now)
	###ORB descriptor
	ORB=cv2.ORB_create(nfeatures=500,
					   scaleFactor=2.0,
					   nlevels=8,
					   edgeThreshold=31,
					   firstLevel=0,
					   WTA_K=2,
					   #scoreType=HARRIS_SCORE,
					   patchSize=31,
					   fastThreshold=20)
	KP1,DES1=ORB.detectAndCompute(IMG_B,None)
	KP2,DES2=ORB.detectAndCompute(IMG_N,None)
	BF=cv2.BFMatcher(normType=cv2.NORM_L2,
					 crossCheck=False)
	MATCHES=BF.knnMatch(DES1,DES2,k=2)
	GOD=[]
	DATA1=[]
	DATA2=[]
	for m,n in MATCHES:
		if m.distance <1* n.distance:
			GOD.append([m])
			IMG1_IDX=m.queryIdx
			IMG2_IDX=m.trainIdx
			(x1,y1)=KP1[IMG1_IDX].pt
			(x2,y2)=KP2[IMG2_IDX].pt
			DATA1.append([x1,y1])
			DATA2.append([x2,y2])
	IMG_R=cv2.drawMatchesKnn(IMG_B,KP1,IMG_N,KP2,GOD,None,flags=2)#
	cv2.imshow("TEST",IMG_R)#
	cv2.waitKey(0)#
	###DBSCAN cluster
	X1=np.array(DATA1)
	X2=np.array(DATA2)
	DB1=DBSCAN(eps=10,min_samples=6).fit(X1)
	DB2=DBSCAN(eps=10,min_samples=6).fit(X2)
	LABEL1=DB1.labels_
	LABEL2=DB2.labels_
	TEMP=np.size(LABEL1,0)
	LABEL_MAX=0
	for i in range(TEMP):
		if LABEL1[i]>LABEL_MAX:
			LABEL_MAX=LABEL1[i]
		if LABEL2[i]>LABEL_MAX:
			LABEL_MAX=LABEL2[i]
	LABEL_ACC=np.zeros((LABEL_MAX+1,LABEL_MAX+1))
	for i in range(TEMP):
		if LABEL1[i]>=0 and LABEL2[i]>=0:
			X_T=LABEL1[i]
			Y_T=LABEL2[i]
			LABEL_ACC[X_T][Y_T]+=1
	MAX_1=0;MAX_2=0;MAX_3=0
	X1=0;Y1=0;X2=0;Y2=0;X3=0;Y3=0
	for i in range(LABEL_MAX+1):
		for j in range(LABEL_MAX+1):
			if LABEL_ACC[i][j]>=MAX_1:
				MAX_3=MAX_2;X3=X2;Y3=Y2
				MAX_2=MAX_1;X2=X1;Y2=Y1
				MAX_1=LABEL_ACC[i][j];X1=i;Y1=j
			elif LABEL_ACC[i][j]>=MAX_2:
				MAX_3=MAX_2;X3=X2;Y3=Y2
				MAX_2=LABEL_ACC[i][j];X2=i;Y2=j
			elif LABEL_ACC[i][j]>=MAX_3:
				MAX_3=LABEL_ACC[i][j];X3=i;Y3=j
	###Affine transform	
	PTS1=[]
	PTS2=[]
	for i in range(TEMP):
		if LABEL1[i]==X1 and LABEL2[i]==Y1:
			PTS1.append(DATA1[i])
			PTS2.append(DATA2[i])
			break
	for i in range(TEMP):
		if LABEL1[i]==X2 and LABEL2[i]==Y2:
			PTS1.append(DATA1[i])
			PTS2.append(DATA2[i])
			break
	for i in range(TEMP):
		if LABEL1[i]==X3 and LABEL2[i]==Y3:
			PTS1.append(DATA1[i])
			PTS2.append(DATA2[i])
			break
	PTS1=np.float32(PTS1)
	PTS2=np.float32(PTS2)
	M=cv2.getAffineTransform(PTS2[0:3],PTS1[0:3])
	#M=np.array([[1.00000000e+00,-0.00000000e+00,0.00000000e+00,
	#[0.00000000e+00,1.00000000e+00,-0.00000000e+00]])
	IMG_RR=cv2.warpAffine(IMG_N,M,(320,240))
	cv2.imshow("RESULT",IMG_RR)#
	cv2.waitKey(0)#
	return 1
'''

