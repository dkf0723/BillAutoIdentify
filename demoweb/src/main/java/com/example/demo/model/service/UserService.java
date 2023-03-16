package com.example.demo.model.service;

import com.example.demo.model.entity.User;
import org.springframework.stereotype.Service;

import java.util.List;

public interface UserService {
    public List<User> findAll();
    public User findByUserId(String id ) ;



    //...
}
