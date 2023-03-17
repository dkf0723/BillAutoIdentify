package com.example.demo.model.service.transformer.impl;

import com.example.demo.model.bean.BillDetailBean;
import com.example.demo.model.entity.BillDetail;
import com.example.demo.model.service.transformer.BillDetailTransformer;
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
