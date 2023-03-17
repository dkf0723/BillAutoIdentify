package com.example.demo.controller;

import com.example.demo.Service.TestService;
import com.example.demo.entity.Test;
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

//    public MyController(TestService testService) {
//        this.testService = testService;
//    }

    @Autowired
    private  TestService testService;


//    @Autowired
//    public MyController(TestService testService) {
//        this.testService = testService;
//    }

    @GetMapping("/hello")
    public List<Test> sayHello() {
        List<Test> tests = testService.findAll();
        logger.info("tests: {}", tests.get(0).getId());
        return tests;
    }
}
