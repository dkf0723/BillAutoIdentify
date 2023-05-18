package com.example.demo.controller;

import com.example.demo.model.bean.BillBean;
import com.example.demo.model.entity.Bill;
import com.example.demo.model.entity.BillDetail;
import com.example.demo.model.entity.User;
import com.example.demo.model.repository.BillDetailRepository;
import com.example.demo.model.service.BillService;
import com.example.demo.model.service.UserService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/bill")
public class MyController {

    private static final Logger logger = LoggerFactory.getLogger(MyController.class);

    @Autowired
    private BillDetailRepository billDetailRepository;

    @Autowired
    private UserService userService;

    @Autowired
    private BillService billService;

    @GetMapping("/hello")
    public String getFruits() {
        JSONObject mainObject = new JSONObject();
        JSONObject subObject = new JSONObject();
        subObject.put("key3", "value3");
        subObject.put("key4", "value4");
        mainObject.put("key1", "value1");
        mainObject.put("key2", subObject);
        String json = mainObject.toString();
        return json;
    }
    @GetMapping("/test")
    public List<BillDetail> test(){
        return billDetailRepository.findByNumberOrderByColumn("MK34758373");
    }
    @GetMapping("/all")
    public List<User> all(){
        return userService.findAll();
    }

    @GetMapping("/check")
    public BillBean check() {
        return billService.findMistakeBill();
    }

    @PostMapping("/check")
    public BillBean checkPost(@RequestBody BillBean billBean) {
        return billService.findMistakeBill(billBean.getPage());
    }

    @PostMapping("/upload")
    public String uploadFile(@RequestParam("file") MultipartFile file) {
        try {
            String fileName = file.getOriginalFilename();
            File destination = new File("C:\\Users\\user\\Desktop\\file\\" + fileName);
            file.transferTo(destination);
            return "File uploaded successfully!";
        } catch (IOException e) {
            e.printStackTrace();
            return "File upload failed.";
        }
    }

}
