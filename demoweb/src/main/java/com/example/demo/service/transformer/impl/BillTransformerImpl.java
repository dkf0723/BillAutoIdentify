package com.example.demo.service.transformer.impl;

import com.example.demo.bean.BillBean;
import com.example.demo.entity.Bill;
import com.example.demo.entity.Customer;
import com.example.demo.service.transformer.BillTransformer;
import org.springframework.beans.BeanUtils;

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
