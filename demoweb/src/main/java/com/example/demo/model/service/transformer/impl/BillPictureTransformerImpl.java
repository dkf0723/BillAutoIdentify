package com.example.demo.model.service.transformer.impl;

import com.example.demo.model.bean.BillPictureBean;
import com.example.demo.model.entity.BillPicture;
import com.example.demo.model.service.transformer.BillPictureTransformer;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Component;

@Component
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
