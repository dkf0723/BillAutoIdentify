package com.example.demo.model.service.impl;

import com.example.demo.model.service.UserService;
import com.example.demo.model.repository.UserRepository;
import com.example.demo.model.entity.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserRepository userRepository;

    @Override
    public List<User> findAll() {
        return userRepository.findAll();
    }

    @Override
    public User findByUserId(String id) {
        return userRepository.findByUserId(id);
    }
}
