package com.example.demo.controller;

import com.example.demo.model.entity.Bill;
import com.example.demo.model.entity.User;
import com.example.demo.model.service.BillService;
import com.example.demo.model.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/bill")
public class MyController {

    private static final Logger logger = LoggerFactory.getLogger(MyController.class);


    @Autowired
    private UserService userService;

    @Autowired
    private BillService billService;

    @GetMapping("/hello")
    public User sayHello() {
        return userService.findByUserId("user1");
    }

    @GetMapping("/check")
    public List<Bill> check() {
        return billService.findMistakeBill();
    }
}
