package com.example.demo.service.transformer.impl;

import com.example.demo.bean.BillDetailBean;
import com.example.demo.entity.BillDetail;
import com.example.demo.entity.Customer;
import com.example.demo.service.transformer.BillDetailTransformer;
import org.springframework.beans.BeanUtils;

public class BillDetailTransformerImpl implements BillDetailTransformer {
    @Override
    public BillDetail transferToEntity(BillDetailBean billDetailBean) {
        BillDetail billDetail = new BillDetail();
        BeanUtils.copyProperties(billDetailBean, billDetail);
        return billDetail;
    }

    @Override
    public BillDetailBean transferToBean(BillDetail billDetail) {
        BillDetailBean billDetailBean = new BillDetailBean();
        BeanUtils.copyProperties(billDetail, billDetailBean);
        return billDetailBean;
    }
}
