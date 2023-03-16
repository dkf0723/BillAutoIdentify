package com.example.demo.Service;

import com.example.demo.Repository.TestRepository;
import com.example.demo.entity.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TestService {

    @Autowired
    private  TestRepository testRepository;

    public List<Test> findAll() {
        return testRepository.findAll();
    }


    //...
}
