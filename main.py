default_encoding = 'utf-8'
from excute import sql_excute
from excute import inbound_order_excute
from  excute import outbound_order_excute
from configdata import configread
from Tools import mySQLutil
from Tools import data_normal
import threading  #模拟多线程

if __name__=="__main__":
    basedata_firstcreat = False
    inorder_creat = False #False
    outorder_creat =  False  #False
    outorder_thr_creat = True
    #########################################################################################################
    #初次创建基础信息数据，获取数据库信息
    if basedata_firstcreat:
        SQL_data = configread.SQL_data()
        db = mySQLutil.sql(SQL_data.host, SQL_data.port, SQL_data.user, SQL_data.passwd, SQL_data.db)
        # 创建仓库信息
        sql_excute.CreatAboutWare(db)
        # 创建货主信息
        sql_excute.CreatAboutShipper(db)
        # 创建其他信息
        sql_excute.CreatAboutOther(db)
        db.db_close()
    #########################################################################################################
    if inorder_creat:
        # 入库订单
        itemnum_style = configread.inbound_mes().itemnum_style  # 使用随机模式还是自定义明细个数模式，0代表随机

        # 普通入库(无容器)
        start = data_normal.get_Normaldata().get_time_new()
        inorder_num = configread.inbound_mes().inordernum
        containertype = 0  # 0为没有容器
        if (inorder_num != 0):
            result1 = inbound_order_excute.new_inboundorder(inorder_num, itemnum_style,containertype)
        end = data_normal.get_Normaldata().get_time_new()
        print(f"普通入库(无容器){inorder_num}创建完成，用时：{int(end) - int(start)}s")
        # 普通入库(有容器)
        start = data_normal.get_Normaldata().get_time_new()
        inordernum_c = configread.inbound_mes().inordernum_c
        containertype = 1  # 0为没有容器
        if (inordernum_c != 0):
            result2 = inbound_order_excute.new_inboundorder(inordernum_c, itemnum_style, containertype)
        end = data_normal.get_Normaldata().get_time_new()
        print(f"普通入库(有容器){inordernum_c}创建完成，用时：{int(end) - int(start)}s")
        # 快速入库(无容器)
        start = data_normal.get_Normaldata().get_time_new()
        fast_inordernum = configread.inbound_mes().fast_inordernum
        containertype = 0  # 0为没有容器
        if (fast_inordernum != 0):
            result3 = inbound_order_excute.newfast_inboundorder(fast_inordernum,itemnum_style, containertype)
        end = data_normal.get_Normaldata().get_time_new()
        print(f"快速入库(无容器){fast_inordernum}创建完成，用时：{int(end) - int(start)}s")
        # 快速入库(有容器)
        start = data_normal.get_Normaldata().get_time_new()
        fast_inordernum_c = configread.inbound_mes().fast_inordernum_c
        containertype = 1  # 0为没有容器
        if (fast_inordernum_c != 0):
            result4 = inbound_order_excute.newfast_inboundorder(fast_inordernum_c,itemnum_style,containertype)
        end = data_normal.get_Normaldata().get_time_new()
        print(f"快速入库(有容器){fast_inordernum_c}创建完成，用时：{int(end) - int(start)}s")
    ##########################################################################################################

    if outorder_creat:
        thr = False
        itemnum_style = configread.outbound_mes().itemnum_style  # 使用随机模式还是自定义明细个数模式，0代表随机
        #创建快速出库订单
        fast_outordernum = configread.outbound_mes().fast_outordernum
        if fast_outordernum!=0:
            out_fresult = outbound_order_excute.newfast_outboundorder(fast_outordernum,itemnum_style,thr)


    # 创建多线程快速出库订单
    if outorder_thr_creat:
        thr = True
        itemnum_style = configread.outbound_mes().itemnum_style  # 使用随机模式还是自定义明细个数模式，0代表随机
        #创建快速出库订单
        fast_outordernum_thr = configread.outbound_mes().fast_outordernum_thr
        if fast_outordernum_thr!=0:
            out_fresult1 = threading.Thread(target=outbound_order_excute.newfast_outboundorder,args=(fast_outordernum_thr,itemnum_style,thr))
            out_fresult1.start()
            out_fresult2 = threading.Thread(target=outbound_order_excute.newfast_outboundorder,args=(fast_outordernum_thr,itemnum_style,thr))
            out_fresult2.start()

