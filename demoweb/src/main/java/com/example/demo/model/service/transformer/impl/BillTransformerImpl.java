package com.example.demo.model.service.transformer.impl;

import com.example.demo.model.bean.BillBean;
import com.example.demo.model.entity.Bill;
import com.example.demo.model.service.transformer.BillTransformer;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Component;

@Component
public class BillTransformerImpl implements BillTransformer {
    @Override
    public Bill transferToEntity(BillBean billBean) {
        Bill bill = new Bill();
        BeanUtils.copyProperties(billBean, bill);
        return bill;
    }

    @Override
    public BillBean transferToBean(Bill bill) {
        BillBean billBean = new BillBean();
        BeanUtils.copyProperties(bill, billBean);
        return billBean;
    }
}
