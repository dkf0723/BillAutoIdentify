package com.example.demo.model.service.transformer.impl;

import com.example.demo.model.bean.UserBean;
import com.example.demo.model.entity.User;
import com.example.demo.model.service.transformer.UserTransformer;
import org.springframework.beans.BeanUtils;
import org.springframework.lang.NonNull;

public class UserTransformerImpl implements UserTransformer {
    @NonNull
    @Override
    public User transferToEntity(@NonNull UserBean userBean) {
        User user = new User();
        BeanUtils.copyProperties(userBean, user);
        return user;
    }

    @NonNull
    @Override
    public UserBean transferToBean(@NonNull User user) {
        UserBean userBean = new UserBean();
        BeanUtils.copyProperties(user, userBean);
       return userBean;
    }
}
