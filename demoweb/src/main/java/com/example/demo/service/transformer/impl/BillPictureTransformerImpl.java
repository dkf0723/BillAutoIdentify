package com.example.demo.service.transformer.impl;

import com.example.demo.bean.BillPictureBean;
import com.example.demo.entity.BillPicture;
import com.example.demo.entity.Customer;
import com.example.demo.service.transformer.BillPictureTransformer;
import org.springframework.beans.BeanUtils;

public class BillPictureTransformerImpl implements BillPictureTransformer {
    @Override
    public BillPicture transferToEntity(BillPictureBean billPictureBean) {
        BillPicture billPicture = new BillPicture();
        BeanUtils.copyProperties(billPictureBean, billPicture);
        return billPicture;
    }

    @Override
    public BillPictureBean transferToBean(BillPicture billPicture) {
        BillPictureBean billPictureBean = new BillPictureBean();
        BeanUtils.copyProperties(billPicture, billPictureBean);
        return billPictureBean;
    }
}
