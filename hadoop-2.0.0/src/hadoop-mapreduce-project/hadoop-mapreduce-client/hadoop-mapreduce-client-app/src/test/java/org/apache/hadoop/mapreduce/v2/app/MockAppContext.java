/**
* Licensed to the Apache Software Foundation (ASF) under one
* or more contributor license agreements.  See the NOTICE file
* distributed with this work for additional information
* regarding copyright ownership.  The ASF licenses this file
* to you under the Apache License, Version 2.0 (the
* "License"); you may not use this file except in compliance
* with the License.  You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

package org.apache.hadoop.mapreduce.v2.app;

import java.util.Map;
import java.util.Set;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.v2.api.records.JobId;
import org.apache.hadoop.mapreduce.v2.app.job.Job;
import org.apache.hadoop.yarn.Clock;
import org.apache.hadoop.yarn.ClusterInfo;
import org.apache.hadoop.yarn.api.records.ApplicationAttemptId;
import org.apache.hadoop.yarn.api.records.ApplicationId;
import org.apache.hadoop.yarn.api.records.impl.pb.ApplicationAttemptIdPBImpl;
import org.apache.hadoop.yarn.event.EventHandler;
import org.apache.hadoop.yarn.security.client.ClientToAMTokenSecretManager;

import com.google.common.collect.Maps;

public class MockAppContext implements AppContext {

  private ApplicationAttemptId createApplicationAttemptId(ApplicationId id, int attempt) {
    ApplicationAttemptIdPBImpl impl = new ApplicationAttemptIdPBImpl();
    impl.setApplicationId(id);
    impl.setAttemptId(attempt);
    return impl;
  }

  final ApplicationAttemptId appAttemptID;
  final ApplicationId appID;
  final String user = MockJobs.newUserName();
  final Map<JobId, Job> jobs;
  final long startTime = System.currentTimeMillis();
  Set<String> blacklistedNodes;

  public MockAppContext(int appid) {
    appID = MockJobs.newAppID(appid);
    appAttemptID = createApplicationAttemptId(appID, 0);
    jobs = null;
  }

  public MockAppContext(int appid, int numTasks, int numAttempts, Path confPath) {
    appID = MockJobs.newAppID(appid);
    appAttemptID = createApplicationAttemptId(appID, 0);
    Map<JobId, Job> map = Maps.newHashMap();
    Job job = MockJobs.newJob(appID, 0, numTasks, numAttempts, confPath);
    map.put(job.getID(), job);
    jobs = map;
  }

  public MockAppContext(int appid, int numJobs, int numTasks, int numAttempts) {
    this(appid, numJobs, numTasks, numAttempts, false);
  }

  public MockAppContext(int appid, int numJobs, int numTasks, int numAttempts,
      boolean hasFailedTasks) {
    appID = MockJobs.newAppID(appid);
    appAttemptID = createApplicationAttemptId(appID, 0);
    jobs = MockJobs.newJobs(appID, numJobs, numTasks, numAttempts, hasFailedTasks);
  }

  @Override
  public ApplicationAttemptId getApplicationAttemptId() {
    return appAttemptID;
  }

  @Override
  public ApplicationId getApplicationID() {
    return appID;
  }

  @Override
  public CharSequence getUser() {
    return user;
  }

  @Override
  public Job getJob(JobId jobID) {
    return jobs.get(jobID);
  }

  @Override
  public Map<JobId, Job> getAllJobs() {
    return jobs; // OK
  }

  @SuppressWarnings("rawtypes")
  @Override
  public EventHandler getEventHandler() {
    return null;
  }

  @Override
  public Clock getClock() {
    return null;
  }

  @Override
  public String getApplicationName() {
    return "TestApp";
  }

  @Override
  public long getStartTime() {
    return startTime;
  }

  @Override
  public ClusterInfo getClusterInfo() {
    return null;
  }

  public ClientToAMTokenSecretManager getClientToAMTokenSecretManager() {
    // Not implemented
    return null;
  }


}
